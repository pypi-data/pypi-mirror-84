import logging
import pandas as pd
import numpy as np

from simulator.send_data_ga.client import SendData

logger = logging.getLogger(__name__)


def pageview(
    df_customers: pd.DataFrame, df_products: pd.DataFrame, interactions: int, ga_viewId: str,
) -> None:

    ga = SendData(
        "ecommerce-raw-bart.website.com", ga_viewId
    )

    for _id in np.arange(0, interactions):
        customer = df_customers.sample().iloc[0]
        product = df_products.sample().iloc[0]

        logger.info(f'\tSend Product {product["sku"]} and Customer {customer["name"]}')

        r = ga.ga_send_pageview(
            f'/products/{product["sku"]}.html',
            f'Bart Recomendation | {product["title"]}',
            product["sku"],
            customer["uuid"],
        )
        logger.info(f"Retorno GA: {r.status_code}")
