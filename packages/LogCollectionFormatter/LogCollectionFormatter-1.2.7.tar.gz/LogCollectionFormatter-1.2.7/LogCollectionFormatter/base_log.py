# coding:utf-8
import json
import logging
import socket
import datetime
import sys
import os
import logging.config
import threading

__all__ = ['MainLog', ]


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back


_srcfile = os.path.normcase(currentframe.__code__.co_filename)


class BaseLog:

    log_levels = ['info', 'debug', 'warn', 'error', 'trace']

    def __init__(self, app_name, prefix_path,  t_code, f_code="", when="D", backup_count=3,
                 journal_log_enable=True):
        if not os.path.exists(prefix_path):
            os.mkdir(prefix_path)
        self.prefix_path = prefix_path
        self.program_log_name = app_name + '_code'
        self.journal_log_name = app_name + '_info'
        self.job_log_name = app_name + '_trace'
        self.host_name = socket.gethostname()
        self.generate_loggers(when, backup_count)
        self.journal_log_enable = journal_log_enable
        self.t_code = t_code

    def generate_loggers(self, when, backup_count):
        pid = str(os.getpid())
        config_dict = dict()
        config_dict['version'] = 1
        config_dict['disable_existing_loggers'] = True
        handler_dict = dict()
        for level in self.log_levels:
            handler_dict[level] = dict()
            handler_dict[level]['class'] = 'logging.handlers.TimedRotatingFileHandler'
            handler_dict[level]['level'] = level.upper() if level != 'trace' else 'DEBUG'
            if level == 'info':
                file_name = self.journal_log_name
            elif level == 'trace':
                file_name = self.job_log_name
            else:
                file_name = self.program_log_name
            handler_dict[level]['filename'] = os.path.join(self.prefix_path, '%s-%s.%s.log' % (file_name, level, pid))
            handler_dict[level]['when'] = when
            handler_dict[level]['backupCount'] = backup_count
            handler_dict[level]['interval'] = 1
            handler_dict[level]['encoding'] = 'utf-8'
        loggers_dict = dict()
        loggers_dict[self.program_log_name] = dict()
        loggers_dict[self.journal_log_name] = dict()
        loggers_dict[self.job_log_name] = dict()
        loggers_dict[self.program_log_name]['handlers'] = ['debug', 'warn', 'error']
        loggers_dict[self.journal_log_name]['handlers'] = ['info']
        loggers_dict[self.job_log_name]['handlers'] = ['trace']
        for logger in loggers_dict.keys():
            loggers_dict[logger]['level'] = 'DEBUG'
            loggers_dict[logger]['propagate'] = False
        config_dict['handlers'] = handler_dict
        config_dict['loggers'] = loggers_dict
        logging.config.dictConfig(config_dict)

    def program_model(self, log_level, message, extra=None):
        path_name, lineno, func_name, logger_module = self.get_current_location()
        data = {
            "app_name": str(self.program_log_name),  # 服务编号
            "logger": str(logger_module),  # 日志对象名
            "HOSTNAME": str(self.host_name),  # 主机名
            "log_time": str(self.date_log_time()),  # 时间
            "level": str(log_level),  # 日志界别
            "thread": str(threading.currentThread().ident),  # 线程编号
            "code_message": str(message[:3000]),  # 消息
            "pathName": str(path_name),  # 打印日志位置
            "lineNo": str(lineno),  # 打印日志行号
            "funcName": str(func_name),  # 打印日志方法名
        }
        if isinstance(extra, dict):
            data.update(extra)
        return json.dumps(data, ensure_ascii=False)

    def trace_model(self, level, extra=None):
        data = {
            "app_name": self.job_log_name,  # 服务编号
            "level": level,
        }
        if isinstance(extra, dict):
            data.update(extra)
        return json.dumps(data, ensure_ascii=False)

    def get_current_location(self):
        try:
            path_name, lineno, func_name = self.find_caller()
        except ValueError:
            path_name, lineno, func_name = "(unknown file)", 0, "(unknown function)"
        try:
            filename = os.path.basename(path_name)
            logger_module = os.path.splitext(filename)[0]
        except (TypeError, ValueError, AttributeError):
            logger_module = "Unknown module"
        return path_name, lineno, func_name, logger_module

    @staticmethod
    def date_log_time():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    @staticmethod
    def find_caller():
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

    def debug(self, msg, *args, **kwargs):
        try:
            msg = msg % args
            message = self.program_model('DEBUG', msg, kwargs.get('extra'))
            logging.getLogger(self.program_log_name).debug(message)
        except Exception as e:
            print(e)

    def info(self, msg, *args, **kwargs):
        try:
            msg = msg % args
            message = self.program_model('INFO', msg, kwargs.get('extra'))
            logging.getLogger(self.program_log_name).debug(message)
        except Exception as e:
            print(e)

    def warn(self, msg, *args, **kwargs):
        try:
            msg = msg % args
            message = self.program_model('WARN',  msg, kwargs.get('extra'))
            logging.getLogger(self.program_log_name).warn(message)
        except Exception as e:
            print(e)

    def error(self, msg, *args, **kwargs):
        try:
            msg = msg % args
            message = self.program_model('ERROR', msg, kwargs.get('extra'))
            logging.getLogger(self.program_log_name).error(message)
        except Exception as e:
            print(e)

    def exception(self, msg, *args, **kwargs):
        try:
            msg = msg % args
            message = self.program_model('ERROR', msg, kwargs.get('extra'))
            logging.getLogger(self.program_log_name).error(message)
        except Exception as e:
            print(e)

    def trace(self, *args, **kwargs):
        try:
            message = self.trace_model('TRACE', kwargs.get('extra'))
            logging.getLogger(self.job_log_name).debug(message, *args, **kwargs)
        except Exception as e:
            print(e)

    def external_log(self,
                     transaction_id,
                     request_url,
                     http_method,
                     request_time,
                     request_headers,
                     request_content,
                     response_headers,
                     response_content,
                     response_time,
                     response_code,
                     http_status_code,
                     total_time,
                     order_id="",
                     account_type="",
                     phone_num="",
                     remark="",
                     method_code="",
                     log_level='INFO',
                     dialog_type='out',
                     f_code=""):
        _, _, _, logger_module = self.get_current_location()
        if len(request_content) > 3000:
            request_content = request_content[:3000]
        if len(response_content) > 3000:
            response_content = response_content[:3000]
        data = {
            "app_name": str(self.journal_log_name),  # 服务编号
            "level": str(log_level),  # 日志界别
            "logger": str(logger_module),  # 日志对象名
            "log_time": str(self.date_log_time()),  # 时间
            "transaction_id": str(transaction_id),
            "dialog_type": str(dialog_type),
            "address": str(request_url),
            "fcode": f_code if dialog_type == 'in' else self.t_code,
            "tcode": self.t_code if dialog_type == 'in' else f_code,
            "method_code": str(method_code or ""),
            "http_method": str(http_method or ""),
            "request_time": request_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "request_headers": str(request_headers),
            "request_payload": str(request_content),
            "response_headers": str(response_headers),
            "response_payload": str(response_content),
            "response_time": response_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "response_code": str(response_code or ""),
            "response_remark": str(remark),
            "http_status_code": str(http_status_code or ""),
            "order_id": str(order_id),
            "account_type": str(account_type),
            "account_num": str(phone_num),
            "province_code": "",
            "city_code": "",
            "key_type": "",
            "key_param": "",
            "total_time": round(float(total_time), 2),
        }
        message = json.dumps(data, ensure_ascii=False)
        logging.getLogger(self.journal_log_name).info(message)

    def customize_log(self, data):
        try:
            if isinstance(data, dict):
                message = json.dumps(data, ensure_ascii=False)
                logging.getLogger(self.journal_log_name).info(message)
            else:
                raise ValueError('传入参数必须为字典')
        except Exception as e:
            self.error(str(e))








