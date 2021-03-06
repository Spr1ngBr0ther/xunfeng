# coding:utf-8
import paramiko
paramiko.util.logging.getLogger('paramiko.transport').addHandler(paramiko.util.logging.NullHandler())

def get_plugin_info():
    plugin_info = {
        "name": "SSH弱口令",
        "info": "直接导致服务器被入侵控制。",
        "level": "紧急",
        "type": "弱口令",
        "author": "wolf@YSRC",
        "url": "",
        "keyword": "server:ssh",
        "source": 1
    }
    return plugin_info

def check(ip, port, timeout):
    success_dict = {}
    # PASSWORD_DIC = ['123456', 'admin', 'test','123123']
    user_list = ['root', 'admin', 'oracle', 'weblogic']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for user in user_list:
        for pass_ in PASSWORD_DIC:
            pass_ = str(pass_.replace('{user}', user))
            try:
                ssh.connect(ip, port, user, pass_, timeout=timeout, allow_agent = False, look_for_keys = False)
                ssh.exec_command('whoami',timeout=timeout)
                if pass_ == '': pass_ = "null"
                success_dict[user] = pass_
                continue 
            except Exception, e:
                if "Unable to connect" in e or "timed out" in e: return
            finally:
                ssh.close()
    return u"存在弱口令 %s" % str(success_dict).lstrip('{').rstrip('}')

# if __name__ == "__main__":
#     check('',22,30)
