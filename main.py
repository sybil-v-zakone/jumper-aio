import asyncio

from modules.module_manager import menu


async def main():
    await menu()

if __name__ == "__main__":
    asyncio.run(main=main())
