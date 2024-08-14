from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.dns_data import DNSData
import pandas as pd

class DataTransformer:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def transform_and_load(self, raw_data):
        # Transformar os dados recebidos da API do Akamai
        df = pd.DataFrame(raw_data)
        aggregated_data = df.groupby(['subscriberId', 'domain']).agg({
            'requests': 'sum',
            'blocks': 'sum'
        }).reset_index()

        # Carregar os dados no PostgreSQL
        session = self.Session()
        for _, row in aggregated_data.iterrows():
            dns_data = DNSData(
                subscriber_id=row['subscriberId'],
                domain=row['domain'],
                requests=row['requests'],
                blocks=row['blocks']
            )
            session.add(dns_data)
        session.commit()

        return aggregated_data
