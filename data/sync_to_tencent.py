#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经验萃取选题数据 - 腾讯文档同步脚本
功能：将GitHub上的提交数据同步到腾讯文档表格

使用方法：
1. 配置腾讯文档API Token（已在 ~/.workbuddy/mcp.json 中配置）
2. 运行此脚本即可同步最新数据到腾讯文档

依赖：pip install requests
"""

import json
import glob
import csv
import os
import sys
from datetime import datetime

# ========== 配置区 ==========
GITHUB_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + '/submissions'
OUTPUT_CSV = os.path.dirname(os.path.abspath(__file__)) + '/经验萃取选题汇总_{date}.csv'

# 腾讯文档配置
TENCENT_DOC_URL = 'https://docs.qq.com/sheet/DTHVjb01zZkFmeUNV'
TENCENT_FILE_ID = 'DTHVjb01zZkFmeUNV'
TENCENT_SHEET_ID = 'BB08J2'

# 腾讯文档表格列顺序（按顺序写入）
COLUMNS = [
    '序号', '姓名', '工号', '部门', '选题', '选题来源',
    '高价值(分)', '紧迫度(分)', '常发生(分)', '三维度总分',
    '萃取价值', '是否有成功案例', '弯路教训', '期望效果', '目标学员',
    '选题是否一目了然', '是否修改选题', '修改后选题', '提交时间', '是否提交报名'
]

# ========== 数据处理函数 ==========
def load_submissions():
    """从GitHub同步的JSON文件中读取所有提交数据"""
    all_data = []
    for f in sorted(glob.glob(os.path.join(GITHUB_DATA_DIR, '*.json'))):
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            all_data.append(data)
    return all_data

def transform_to_tencent_format(data_list):
    """将数据转换为腾讯文档表格格式（按列顺序）"""
    rows = []
    for idx, d in enumerate(data_list, start=1):
        # 计算三维度总分
        dim1 = int(d.get('dim1Score', 0) or 0)
        dim2 = int(d.get('dim2Score', 0) or 0)
        dim3 = int(d.get('dim3Score', 0) or 0)
        total_score = dim1 + dim2 + dim3

        # 是否验证
        verification_status = d.get('verificationStatus', '')
        if not verification_status:
            topic = d.get('topic', '')
            if topic and topic not in ['12345', 'test', '']:
                verification_status = '完成验证'
            else:
                verification_status = '需要重写'

        # 是否提交报名（空=未提交，是=已提交）
        enroll_status = d.get('enrollStatus', '')
        enroll_status_text = '是' if enroll_status == '是' else ''

        # 选题是否清晰 -> 选题是否一目了然
        is_clear = d.get('isClear', '')
        is_clear_map = {
            'yes': '是',
            'somewhat': '部分清晰',
            'no': '否',
            '是': '是',
            '部分清晰': '部分清晰',
            '否': '否'
        }
        is_clear_text = is_clear_map.get(is_clear, is_clear)

        # 是否修改选题
        need_revise = '是' if d.get('needRevise') == 'yes' else '否'

        # 是否有成功案例
        has_case = '是' if d.get('hasCase') == 'yes' else '否'

        row = [
            idx,                          # 序号
            d.get('name', ''),           # 姓名
            d.get('employeeId', ''),     # 工号
            d.get('department', ''),     # 部门
            d.get('topic', ''),          # 选题
            d.get('source', ''),         # 选题来源
            dim1,                         # 高价值(分)
            dim2,                         # 紧迫度(分)
            dim3,                         # 常发生(分)
            total_score,                  # 三维度总分
            d.get('extractionValue', ''), # 萃取价值
            has_case,                     # 是否有成功案例
            d.get('lessonLearned', ''),   # 弯路教训
            d.get('expectedEffect', ''), # 期望效果
            d.get('targetAudience', ''),  # 目标学员
            is_clear_text,                # 选题是否一目了然
            need_revise,                  # 是否修改选题
            d.get('revisedTopic', ''),   # 修改后选题
            d.get('submitTime', ''),      # 提交时间
            enroll_status_text            # 是否提交报名
        ]
        rows.append(row)
    return rows

def export_to_csv(rows, output_path):
    """导出为CSV文件"""
    if not rows:
        print('⚠️ 没有数据可导出')
        return False

    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)  # 写入表头
        writer.writerows(rows)

    print(f'✅ CSV文件已生成: {output_path}')
    return True

# ========== 主程序 ==========
def main():
    print('=' * 50)
    print('📊 经验萃取选题数据 - 腾讯文档同步')
    print('=' * 50)
    print()

    # 1. 读取数据
    print('📂 正在读取GitHub同步数据...')
    all_data = load_submissions()
    print(f'   共找到 {len(all_data)} 条记录')

    if not all_data:
        print('⚠️ 没有找到任何提交数据')
        return

    # 2. 转换格式
    print('🔄 正在转换数据格式...')
    rows = transform_to_tencent_format(all_data)

    # 3. 导出CSV（备份）
    today = datetime.now().strftime('%Y%m%d')
    output_path = OUTPUT_CSV.format(date=today)
    export_to_csv(rows, output_path)

    # 4. 打印数据供人工核对
    print()
    print('📋 数据预览（前3条）:')
    for i, row in enumerate(rows[:3], 1):
        print(f'   {i}. {row[1]} | {row[2]} | {row[4]}')

    print()
    print('=' * 50)
    print(f'📎 腾讯文档链接: {TENCENT_DOC_URL}')
    print('=' * 50)
    print()
    print('💡 提示: 数据已准备好，请通过 MCP 工具同步到腾讯文档')
    print(f'   - 文件ID: {TENCENT_FILE_ID}')
    print(f'   - 工作表ID: {TENCENT_SHEET_ID}')
    print(f'   - 数据行数: {len(rows)}')

if __name__ == '__main__':
    main()
