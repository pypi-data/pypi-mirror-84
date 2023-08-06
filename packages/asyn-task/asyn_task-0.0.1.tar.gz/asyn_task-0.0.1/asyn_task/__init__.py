# coding:utf-8
__author__ = "zhp"
# create by zhp on 2020/11/02
import hashlib
import cloudpickle
import multiprocessing
import os
import time
import random
import string
import json
import sys
import base64
import datetime
import psutil
from .log import get_logger

try:
    logger = get_logger('/tmp/asyn_task.log',3)
except:
    logger = None


def log(message):
    if logger:
        logger.info(message)



_current_dir = os.path.abspath(os.path.dirname(__file__))
_my_path = os.path.join(_current_dir, 'process_task.py')
if sys.executable.endswith('python') or sys.executable.endswith('python3'):
    _py_path = sys.executable
elif sys.executable.endswith('uwsgi') or sys.executable.endswith('uwsgi3'):
    if sys.version_info.major == 2:
        _py_path = os.path.join(os.path.dirname(sys.executable), 'python2')
        if not  os.path.exists(_py_path):
            _py_path = 'python2'
    else:
        _py_path = os.path.join(os.path.dirname(sys.executable), 'python3')
        if not os.path.exists(_py_path):
            _py_path = 'python3'
else:
    _py_path = 'python%s' % sys.version_info.major


def run_task(fun, args=(), kwargs={}):
    def _gen(length: int = 8):
        "生成随机字符串"
        _ = random.sample(string.ascii_letters[:26] + "0123456789", length)
        return "".join(_)
    task_id = _gen(10)
    fun = cloudpickle.dumps(fun)
    fun_b64 = base64.b64encode(fun).decode()
    data = {"fun_b64":fun_b64, 'args': args, 'kwargs': kwargs}
    log(data)
    # print(data)
    data_json = json.dumps(data)
    os.system("mkdir -p /tmp/process_task")
    os.system("mkdir -p /tmp/process_task_log")
    os.system("mkdir -p /tmp/process_task_result")

    # 对于过老的log删除掉
    for i in  os.listdir('/tmp/process_task_log'):
        if i.endswith(".log"):
            _real_path = os.path.join('/tmp/process_task_log', i)
            try:
                modify_time = os.path.getmtime(_real_path)
                if time.time() - modify_time >= 86400*2:
                    os.system("rm -rf %s" % _real_path)
            except:
                pass

    # 对于过老的result删除掉
    for i in  os.listdir('/tmp/process_task_result'):
        if i.endswith(".log"):
            _real_path = os.path.join('/tmp/process_task_result', i)
            try:
                modify_time = os.path.getmtime(_real_path)
                if time.time() - modify_time >= 86400*2:
                    os.system("rm -rf %s" % _real_path)
            except:
                pass


    with open("/tmp/process_task/%s" % task_id, "w") as f:
        f.write(data_json)

    os.system("%s %s/process_task.py %s >> /tmp/process_task_log/%s.log 2>&1" %
              (_py_path, _current_dir, task_id, task_id))
    log('任务id%s'%task_id)
    return task_id


def is_running(task_id):
    _p = psutil.Process(pid=1)
    for i in _p.children():
        try:
            cmdline = i.cmdline()
            if task_id == cmdline[-1]:
                return True
        except:
            pass
    return False

def get_result(task_id):
    if is_running(task_id):
        raise Exception('task is running!')
    else:
        if os.path.exists("/tmp/process_task_result/%s" % task_id):
            with open("/tmp/process_task_result/%s" % task_id, "r") as f:
                return json.loads(f.read())
        else:
            return None

if __name__ == '__main__':
    import daemon
    task_id = sys.argv[-1]
    with open("/tmp/process_task/%s" % task_id, "r") as f:
        data_json = f.read()
    os.system("rm -rf /tmp/process_task/%s" % task_id)
    data = json.loads(data_json)
    fun = cloudpickle.loads(base64.b64decode(data['fun_b64'].encode()))
    args = data['args']
    kwargs = data['kwargs']
    # print(args,kwargs)
    daemon.daemon_start()
    result = fun(*args, **kwargs)
    result_json = json.dumps(result)
    os.system("mkdir -p /tmp/process_task_result")
    with open("/tmp/process_task_result/%s" % task_id, "w") as f:
        f.write(result_json)