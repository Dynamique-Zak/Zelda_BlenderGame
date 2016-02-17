import datetime

from conf import *
        
class WriteUtils:

    @staticmethod
    def getHeaderScript():
        developper = DX_BGE.developper
        now = datetime.datetime.now()
        now_str = now.strftime("%d/%m/%y at %H:%M")

        info = "#===================================================" \
        "\n# * Author : " + developper['author'] + " " \
        "\n# * Mail : " + developper['email'] + " " \
        "\n# * Role : " + developper['role'] + " " \
        "\n# * Created " + now_str + " " \
        "\n#===================================================\n" \

        return info
