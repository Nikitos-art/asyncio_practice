###--------------------------------with out asyncio -----------------------------------#####
# import time
# import itertools
# import sys
# import threading
#
#
# class Signal:
#     go = True
#
#
# def spin(msg, signal):
#     write, flush = sys.stdout.write, sys.stdout.flush
#     for char in itertools.cycle('|/-\\'):
#         status = char + ' ' + msg
#         write(status)
#         flush()
#         write('\x08' * len(status))
#         time.sleep(.1)
#         if not signal.go:
#             break
#     write(' ' * len(status) + '\x08' * len(status))
#
#
# def slow_function():
#     # pretend waiting a long time for I/O
#     time.sleep(3)
#     return 42
#
#
# def supervisor():
#     signal = Signal()
#     spinner = threading.Thread(target=spin,
#                                args=('thinking!', signal))
#     print('spinner object:', spinner)
#     spinner.start()
#     result = slow_function()
#     signal.go = False
#     spinner.join()
#     return result
#
#
# def main():
#     result = supervisor()
#     print('Answer:', result)
#
#
# if __name__ == '__main__':
#     main()
####-------------------------------------- with asyncio ------------------------------------------###
import asyncio
import itertools
import sys


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin('thinking!'))
    print('spinner object:', spinner)
    result = await slow_function()
    spinner.cancel()
    return result


async def main():
    result = await supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    asyncio.run(main())
