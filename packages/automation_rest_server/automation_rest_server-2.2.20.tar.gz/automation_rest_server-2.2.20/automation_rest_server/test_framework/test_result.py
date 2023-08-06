# coding=utf-8
import os
import  xml.dom.minidom
from utils.system import get_ip_address

class TestResult(object):


    def __init__(self):
        pass

    def _get_log_txt(self, log_path):
        file_ = open(log_path)
        txt_ = file_.read()
        file_.close()
        return txt_

    def get_xml_report_txt(self, xml_path):
        dom = xml.dom.minidom.parse(xml_path)
        root = dom.documentElement
        system_out_element = root.getElementsByTagName('system-out')
        system_out_tex = system_out_element[0].firstChild.wholeText if system_out_element else ""
        fail_element = root.getElementsByTagName('failure')
        fail_txt = fail_element[0].firstChild.wholeText if fail_element else ""
        error_element = root.getElementsByTagName('error')
        error_txt = error_element[0].firstChild.wholeText if error_element else ""
        sys_error_element = root.getElementsByTagName('system-err')
        sys_error_txt = sys_error_element[0].firstChild.wholeText if sys_error_element else ""
        xml_logs = system_out_tex + fail_txt + error_txt + sys_error_txt
        return xml_logs

    def get_log(self, logs):
        log = str()
        try:
            for item in logs:
                log_content = self._get_log_txt(item)
                log = "{} \n\n{}\n\n{}".format(log, item, log_content)
        except Exception as all_exception:
            print(all_exception)
        return log

    def get_test_suite_test_msg(self, test_results):
        msg = ""
        if test_results is not None:
            for test_result in test_results:
                if "xml_path" in test_result.keys():
                    xml_log = self.get_xml_logs(test_result["xml_path"])
                    msg = msg + "\n \n ****************************************** \n \n"
                    msg = msg + test_result["name"] + "\n"
                    msg = msg + "\n" + xml_log
                elif "msg" in test_result.keys():
                    msg = msg + str(test_result["msg"])
                elif "log" in test_result.keys():
                    logs = test_result["log"]
                    msg = msg + str(self.get_log(logs))
                elif "log_path" in test_result.keys():
                    msg = msg + str(self._get_log_txt(test_result["log_path"]))
        return msg

    @staticmethod
    def check_xml_file_size(path):
        file_size = os.path.getsize(path)
        result = True if file_size < 1*1000*1000 else False
        return result

    def get_xml_logs(self, log_path):
        if self.check_xml_file_size(log_path):
            xml_log = self.get_xml_report_txt(log_path)
        else:
            xml_log = "log file more than 1M, do not upload file.\n" \
                      "logs at host: {}, path: {}".format(get_ip_address(), log_path)
        return xml_log
