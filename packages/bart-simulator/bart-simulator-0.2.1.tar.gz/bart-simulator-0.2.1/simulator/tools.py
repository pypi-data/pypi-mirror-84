"""  """
import logging
import pkg_resources
import argparse
import os
import sys
import pandas as pd
from random import randint

from simulator.generate import datasets
from simulator.send_data_ga import data_types


base_path = os.getcwd()


def tools_parser(sargs):
    parser = argparse.ArgumentParser(
        description="Send event views to Google Analytics and Generator "
        "customers or products data-set (bart-recs CLI)"
    )
    parser.add_argument("--loglevel", default="INFO")

    packtools_version = pkg_resources.get_distribution("bart-simulator").version
    parser.add_argument("--version", action="version", version=packtools_version)

    subparsers = parser.add_subparsers(title="Commands", metavar="", dest="command")

    # GENERATION Datasets
    parents_generation = argparse.ArgumentParser(add_help=False)
    parents_generation.add_argument(
        "script",
        choices=["customers", "products"],
        help="Arquivo que sera gerado pelo processo",
    )
    parents_generation.add_argument(
        "--desc-path",
        "-d",
        default=base_path,
        help="Pasta onde sera salvo os dataset gerados",
    )
    parents_generation.add_argument(
        "--rows", "-r", default=1000, help="Quantidades de Linhas geradas", type=int,
    )
    parents_generation.add_argument(
        "--format",
        "-f",
        default="csv",
        choices=["csv", "json"],
        nargs="+",
        help="Formato do arquivo de saida que sera salvo, "
        "pode ser adiciona mais de um tipo ao mesmo tempo ",
        required=True,
    )

    subparsers.add_parser(
        "generation",
        help="Gera os data set simulados para as recomendações",
        parents=[parents_generation,],
    )

    # Send Ping GA
    parents_send_data_ga = argparse.ArgumentParser(add_help=False)
    parents_send_data_ga.add_argument(
        "event", choices=["pageview",], help="Tipo de evento que sera enviado ao GA",
    )
    parents_send_data_ga.add_argument(
        "--ga-track-id",
        "-gaId",
        help="Id de acompanhamento para o sua conta do GA",
    )

    parents_send_data_ga.add_argument(
        "--customers",
        "-c",
        required=True,
        help="Caminho para o dataset de customers, em csv",
    )
    parents_send_data_ga.add_argument(
        "--products",
        "-p",
        required=True,
        help="Caminho para o dataset de products, em csv",
    )
    parents_send_data_ga.add_argument(
        "--interactions", "-i", help="Quantidades de interações geradas", type=int,
    )
    parents_send_data_ga.add_argument(
        "--random-interactions",
        help="Gerar uma quantidades de interações randomicas",
        action="store_true",
    )

    subparsers.add_parser(
        "send-data-ga",
        help="Envia dados simulados para o Google Analytics",
        parents=[parents_send_data_ga,],
    )

    ################################################################################################
    args = parser.parse_args(sargs)

    # CHANGE LOGGER
    level = getattr(logging, args.loglevel.upper())
    logger = logging.getLogger()
    logger.setLevel(level)

    if args.command == "generation":
        logger.info("Iniciando o processamento...")

        func = getattr(datasets, args.script)
        logger.info(f"Gerando arquivo {args.script}")
        dataset = func(args.rows)

        if "csv" in args.format:
            dataset.to_csv(os.path.join(args.desc_path, f"{args.script}.csv"))
            logger.info("Arquivo csv salvo com sucesso!")

        if "json" in args.format:
            dataset.to_json(
                os.path.join(args.desc_path, f"{args.script}.json"),
                orient="records",
                indent=4,
            )
            logger.info("Arquivo json salvo com sucesso!")
        logger.info(
            f"Processamento Finalizado, arquivos salvos na pasta {args.desc_path}"
        )

    elif args.command == "send-data-ga":
        logger.info("Iniciando o processamento...")

        if not args.random_interactions and not args.interactions:
            logger.error(
                "Umas das duas opções deve ser determinada"
                "'--interactions' ou '--random-interactions' deve ser OBRIGATORIO"
            )
            sys.exit()

        func = getattr(data_types, args.event)
        if args.random_interactions:
            interactions = randint(100, 1000)
        else:
            interactions = args.interactions

        result = func(
            df_customers=pd.read_csv(args.customers),
            df_products=pd.read_csv(args.products),
            interactions=interactions,
            ga_viewId=args.ga_track_id,
        )
        logger.info(
            f"Processamento Finalizado, Enviado {args.interactions} {args.event} para o GA"
        )

    else:
        raise SystemExit(
            "Vc deve escolher algum parametro, ou '--help' ou '-h' para ajuda"
        )

    return 0
