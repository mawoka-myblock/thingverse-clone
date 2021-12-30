from asyncio import run
from helpers.bgtasks import copy_to_typesense, migrate_existing

# run(copy_to_typesense())
run(migrate_existing())