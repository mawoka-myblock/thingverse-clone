from asyncio import run
from helpers.bgtasks import copy_to_typesense

run(copy_to_typesense())