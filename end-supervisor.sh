#!/usr/bin/env bash
ps -ef |grep supervisor/crawl_supervisor.conf |awk '{print $2}'|xargs kill -9

