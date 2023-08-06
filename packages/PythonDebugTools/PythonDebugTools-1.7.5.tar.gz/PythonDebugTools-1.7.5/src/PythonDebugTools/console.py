import pprint
import traceback




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']
debug = __debug__

pp = pprint.PrettyPrinter(indent=4)
def PRINT(title: str, *args, **kwargs):
    if not debug: return
    print(f"\n ---------------- {title} ---------------- \n\r")
    pp.pprint(dict(args=args, kwargs=kwargs))



def getPPrintStr(Object: any) -> str: return f'{pp.pformat(Object)}'



def print_exception(e: Exception):
    if not debug: return
    traceback.print_exception(type(e), e, e.__traceback__)
