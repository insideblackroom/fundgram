from . import cli, botcli
import asyncio

async def main():
    from ._misc import _basewrapp
    import consumers
    await cli.send_message('me', 'test 2')
    await botcli.run_until_disconnected()

if __name__ == '__main__':
    cli.run_in_loop(main())


