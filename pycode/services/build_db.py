from db_builder import create_static_types, manage_company, manage_audience, manage_touchpoints, manage_campaign
from neo4j.v1 import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687')


def create_static():
    create_static_types.create_static()


def create_company():
    manage_company.read_csv('./source_data/company.csv')


def create_audience():
    manage_audience.read_csv_user('./source_data/audience.csv')


def create_campaign():
    manage_campaign.read_csv_campaign('./source_data/campaign.csv')


def create_touchpoints():
    manage_touchpoints.create_touchpoint("EMAIL", "SendGrid")
    manage_touchpoints.create_touchpoint("EMAIL", "MailChimp")


def create_audience_grp():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("""                               
                MATCH (a :audience) Where a.income <> ""
                MATCH (i :INCOME_GROUP) WHERE i.ref = a.income
                CREATE (a)-[b :IN_INCOME_BAND]->(i)
                return b
            """)
        with session.begin_transaction() as tx:
            tx.run("""                               
                MATCH (a :audience) Where a.aud IN [ 'A', 'B', 'C', 'D']
                MATCH (i :AUDIENCE_GROUP) WHERE i.ref = a.aud
                CREATE (a)-[b :IN_AUDIENCE]->(i)
                return b
            """)


def create_company_profile():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("""
                MATCH (a :company) Where a.industry <> ""
                MATCH (i :INDUSTRY) WHERE i.title = a.industry
                CREATE (a)-[b :IN_INDUSTRY]->(i)
                return b
                """)
            tx.run("""
                MATCH (a :company) Where a.company_id <> ""
                MATCH (i :campaign) WHERE i.company_id = a.company_id
                CREATE (a)-[b :CAMPAIGN_SPONSOR]->(i)
                return b
                """)


def create_campaign_profile():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("""
                MATCH (a :campaign) Where a.target <> ""
                MATCH (i :MARKETING_TARGET) WHERE i.title = a.target
                CREATE (a)-[b :TARGET_TYPE]->(i)
                return b
            """)
            tx.run("""
                MATCH (a :campaign) Where a.name <> ''
                MATCH (i :company) WHERE i.name = a.name
                CREATE (a)-[b :CAMPAIGN_CLIENT]->(i)
                return b
            """)
            tx.run("""
                MATCH (a :campaign) Where a.audience <> ''
                MATCH (i :AUDIENCE_GROUP) WHERE i.ref = a.audience
                CREATE (a)-[b :CAMPAIGN_AUDIENCE]->(i)
                return b
            """)
            tx.run("""                               
                MATCH (a :campaign) Where a.type <> ''
                MATCH (i :touchpoint) WHERE i.type = a.type
                CREATE (a)-[b :CAMPAIGN_TOUCHPOINT]->(i)
                return b
            """)


def main():
    create_static()
    create_company()
    create_audience()
    create_campaign()
    create_audience_grp()
    create_campaign_profile()
    create_company_profile()


if __name__ == "__main__":
    main()
