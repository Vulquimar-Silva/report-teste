import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.core.database import db
from src.models.dns_data import DNSData

class DataTransformer:
    """
    Realiza a transformação e o carregamento de dados no banco (ETL).
    Agora não descarta campos extras (ex: company_name, period, etc.).
    """
    def __init__(self, api_type='akamai'):
        self.logger = logging.getLogger(__name__)
        self.api_type = api_type.lower()

    def transform_and_load(self, raw_data):
        """
        Transforma os dados brutos e carrega no banco de dados.

        Retorna:
          (aggregated_data, df_raw)
            aggregated_data: DataFrame com subscriberId/domain/requests/blocks agregados
            df_raw: DataFrame bruto com todas as colunas (company_name, period etc.)
        """
        self.logger.info(f"Iniciando transformação e carregamento para a API '{self.api_type}'...")

        if not isinstance(raw_data, list) or not raw_data:
            self.logger.error("Os dados de entrada estão vazios ou não são uma lista válida.")
            raise ValueError("Dados de entrada inválidos. Esperado uma lista de registros (list).")

        # 1) DataFrame bruto com todos os campos
        df_raw = pd.DataFrame(raw_data)
        self.logger.info(f"DataFrame bruto criado com {df_raw.shape[0]} registros. Colunas: {df_raw.columns.tolist()}")

        # Verifica quais campos precisamos para aggregator DNS
        if self.api_type == 'fake':
            required_columns = {'subscriberId', 'domain', 'requests', 'blocked'}
            column_mapping = {'blocked': 'blocks'}
        elif self.api_type == 'akamai':
            required_columns = {'subscriberId', 'domain', 'requests', 'blocks'}
            column_mapping = {}
        else:
            self.logger.error(f"Tipo de API desconhecido: {self.api_type}")
            raise ValueError(f"Tipo de API desconhecido: {self.api_type}")

        valid_rows = []
        for record in raw_data:
            if all(col in record for col in required_columns):
                # Renomear colunas, se necessário
                new_record = {}
                for k, v in record.items():
                    new_key = column_mapping.get(k, k)
                    new_record[new_key] = v
                valid_rows.append(new_record)

        if not valid_rows:
            self.logger.error("Nenhum registro válido encontrado para aggregator (DNS).")
            raise ValueError(f"Os dados devem conter as colunas mínimas: {required_columns}")

        # 2) DataFrame específico para aggregator DNS
        df_dns = pd.DataFrame(valid_rows)
        self.logger.info(f"{len(valid_rows)} registros válidos para aggregator DNS. Colunas: {df_dns.columns.tolist()}")

        # Agrega requests e blocks
        try:
            aggregated_data = df_dns.groupby(['subscriberId', 'domain']).agg({
                'requests': 'sum',
                'blocks': 'sum'
            }).reset_index()

            self.logger.info("Aggregator de DNS concluído com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao agrupar/transformar dados DNS: {e}")
            raise ValueError("Erro durante a transformação dos dados DNS.") from e

        # Carrega no banco DNSData
        try:
            for _, row in aggregated_data.iterrows():
                dns_data = DNSData.query.filter_by(
                    company_id=row['subscriberId'],
                    domain=row['domain']
                ).first()

                if dns_data:
                    dns_data.requests += row['requests']
                    dns_data.blocks += row['blocks']
                else:
                    new_dns = DNSData(
                        company_id=row['subscriberId'],
                        domain=row['domain'],
                        requests=row['requests'],
                        blocks=row['blocks']
                    )
                    db.session.add(new_dns)

            db.session.commit()
            self.logger.info("DNSData carregado com sucesso no banco de dados.")
        except SQLAlchemyError as e:
            db.session.rollback()
            self.logger.error(f"Erro ao carregar dados no banco: {e}")
            raise

        # Retorna DOIS DataFrames: (aggregated_data, df_raw)
        return (aggregated_data, df_raw)
