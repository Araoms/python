##############################################
# 基于centos7构建python3运行环境
# 进入容器：docker exec -it connorflow /bin/bash
##############################################

FROM centos:centos7
MAINTAINER connorflow

RUN yum -y update; yum clean all
# 没有这一步将安装nginx失败
RUN yum -y install epel-release tar ; yum clean all
RUN yum -y install nginx ; yum clean all

RUN set -ex \
    # 预安装所需组件
    && yum install -y wget tar libmysqlclient-dev supervisor libffi-devel zlib-devel bzip2-devel openssl-devel openldap24-libs openldap openldap-clients openldap-devel  ncurses-devel sqlite-devel readline-devel tk-devel gcc initscripts mysql-devel\
    && wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz \
    && tar -zxvf Python-3.6.4.tgz \
    && cd Python-3.6.4 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && rm -rf /Python-3.6.4* \
    && yum install -y epel-release \
    && yum install -y python-pip
# 设置默认为python3
RUN set -ex \
    # 备份旧版本python
    #&& mv /usr/bin/python /usr/bin/python27 \
    #&& mv /usr/bin/pip /usr/bin/pip-python2.7 \
    # 配置默认为python3
    && ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3 \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
# 修复因修改python版本导致yum失效问题
#RUN set -ex \
#    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
#    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down \
#    && yum install -y deltarpm
# 基础环境配置
RUN set -ex \
    # 修改系统时区为东八区
    && rm -rf /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum install -y vim \
    # 安装定时任务组件
    && yum -y install cronie
# 支持中文
RUN yum install kde-l10n-Chinese -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 更新pip版本
RUN pip3 install --upgrade pip
ENV LC_ALL zh_CN.UTF-8

# uwsgi
RUN pip3 install -i https://pypi.doubanio.com/simple/ uwsgi
RUN set -ex \
                                && ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
# 环境变量
ENV MYSQL_DATABASE_NAME connorflow
ENV EMAIL_HOST_USER a37free@163.com
ENV EMAIL_HOST_PASSWORD 123456

# nginx、supervisor配置  
COPY supervisor-app.ini /etc/supervisord.d/

# 安装项目所需python第三方库
COPY requirements.txt /home/docker/code/connorflow/
RUN pip3 install -i https://pypi.doubanio.com/simple/ \
	 -r /home/docker/code/connorflow/requirements.txt

# uwsgi.ini 及 uwsgi_params
COPY . /home/docker/code/

EXPOSE 80
CMD ["supervisord", "-n"]
