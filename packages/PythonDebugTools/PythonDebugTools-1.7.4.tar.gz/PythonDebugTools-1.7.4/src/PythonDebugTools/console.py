import pprint
import traceback




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']

pp = pprint.PrettyPrinter(indent=4)
def PRINT(title: str, *args, **kwargs):
    print(f"\n ---------------- {title} ---------------- \n\r")
    pp.pprint(dict(args=args, kwargs=kwargs))



def getPPrintStr(Object: any) -> str: return f'{pp.pformat(Object)}'



def print_exception(e: Exception): traceback.print_exception(type(e), e, e.__traceback__)
