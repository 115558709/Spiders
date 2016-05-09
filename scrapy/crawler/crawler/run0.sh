#!/usr/bin/env bash
rm -f tb
scrapy runspider  --logfile=tb spiders/taobao.py