# GlobalCloud 项目群统一命令入口（项目群规范化 02）
# 命令来源：无（全部为占位，待补真实入口）
# 说明：未识别到真实命令的目标显示“待配置”，请按 README 命令段补充；不要在此臆造命令。

PYTHON ?= python3
GC_STANDARD ?= /Users/lujunxiang/Projects/GlobalCloud V0.0.1/_governance/tools/gc_standard.py

.PHONY: help setup dev test build validate clean

help:
	@echo "GlobalCloud GPCF 常用命令："
	@echo "  make setup      安装依赖"
	@echo "  make dev        启动开发"
	@echo "  make test       运行测试"
	@echo "  make build      构建"
	@echo "  make validate   项目群统一规范检查（R01-R20）"
	@echo "  make clean      清理产物"

setup:  # 安装依赖（占位）
	@echo "待配置：见 README 命令段（setup）"

dev:  # 启动开发（占位）
	@echo "待配置：见 README 命令段（dev）"

test:  # 运行测试（占位）
	@echo "待配置：见 README 命令段（test）"

build:  # 构建（占位）
	@echo "待配置：见 README 命令段（build）"

validate:
	"$(PYTHON)" "$(GC_STANDARD)" check --repo "GlobalCloud GPCF" --fail-on error

clean:
	@echo "待配置：见 README 命令段（clean）"
