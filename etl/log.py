# coding=utf-8
import logging
import os
import time
from datetime import datetime

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL, }

logger = logging.getLogger()
level = 'default'
dateformat = '%Y-%m-%d %H:%M:%S'
today = int(datetime.strftime(datetime.today(), '%Y%m%d'))

def createFile(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        # 创建并打开一个新文件
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()


class Log(object):

    def __init__(self, fp, date):
        log_filename = r'%s/%s_update.log' % (fp, date)
        logger.setLevel(LEVELS.get(level, logging.NOTSET))
        createFile(log_filename)

        # 注意文件内容写入时编码格式指定

        self.dateformat = '%Y-%m-%d %H:%M:%S'
        self.handler = logging.FileHandler(log_filename, encoding='utf-8')

    def debug(self, log_message):
        self.setHandler('debug')
        logger.debug("[DEBUG " + self.getCurrentTime() + "]" + log_message)
        self.removerhandler('debug')

    def info(self, log_message):
        self.setHandler('info')
        logger.info("[INFO " + self.getCurrentTime() + "]" + log_message)
        self.removerhandler('info')

    def warning(self, log_message):
        self.setHandler('warning')
        logger.warning("[WARNING " + self.getCurrentTime() + "]" + log_message)
        self.removerhandler('warning')

    def error(self, log_message):
        self.setHandler('error')
        logger.error("[ERROR " + self.getCurrentTime() + "]" + log_message)
        self.removerhandler('error')

    def critical(self, log_message):
        self.setHandler('critical')
        logger.critical("[CRITICAL " + self.getCurrentTime() + "]" + log_message)
        self.removerhandler('critical')

    def setHandler(self,level):
        logger.addHandler(self.handler)


    def removerhandler(self,level):
        if level == 'error':
            logger.removeHandler(self.handler)
        logger.removeHandler(self.handler)


    def getCurrentTime(self,):
        return time.strftime(self.dateformat, time.localtime(time.time()))


# logger可以看做是一个记录日志的人，对于记录的每个日志，他需要有一套规则，比如记录的格式（formatter），
# 等级（level）等等，这个规则就是handler。使用logger.addHandler(handler)添加多个规则，
# 就可以让一个logger记录多个日志。



if __name__ == "__main__":
    mylog = Log(r'E:/data', today)
    mylog.debug("This is debug message")
    mylog.info("This is info message")
    mylog.warning("This is warning message")
    mylog.error("This is error message")
    mylog.critical("This is critical message")