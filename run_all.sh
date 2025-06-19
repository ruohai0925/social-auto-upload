#!/bin/bash

echo "=== 开始执行自动化上传脚本 ==="
echo "时间: $(date)"
echo ""

source $(conda info --base)/etc/profile.d/conda.sh
conda activate social-auto-upload

echo "已激活 conda 环境: social-auto-upload"
echo ""

# 首先运行一遍所有cookie，确保cookie有效，否则报错退出
echo "=== 第一步: 检查所有平台的Cookie状态 ==="

echo "检查快手Cookie..."
if python get_kuaishou_cookie.py; then
    echo "✓ 快手Cookie检查完成"
else
    echo "✗ 快手Cookie检查失败"
    exit 1
fi

echo "检查抖音Cookie..."
if python get_douyin_cookie.py; then
    echo "✓ 抖音Cookie检查完成"
else
    echo "✗ 抖音Cookie检查失败"
    exit 1
fi

echo "检查腾讯视频Cookie..."
if python get_tencent_cookie.py; then
    echo "✓ 腾讯视频Cookie检查完成"
else
    echo "✗ 腾讯视频Cookie检查失败"
    exit 1
fi

echo "检查小红书Cookie..."
if python get_xiaohongshu_cookie.py; then
    echo "✓ 小红书Cookie检查完成"
else
    echo "✗ 小红书Cookie检查失败"
    exit 1
fi

#./biliup -u account.json login

echo ""
echo "=== 第二步: 开始上传视频到各平台 ==="

echo "上传到快手..."
if python upload_video_to_kuaishou.py; then
    echo "✓ 快手上传完成"
else
    echo "✗ 快手上传失败"
fi

echo "上传到抖音..."
if python upload_video_to_douyin.py; then
    echo "✓ 抖音上传完成"
else
    echo "✗ 抖音上传失败"
fi

echo "上传到腾讯视频..."
if python upload_video_to_tencent.py; then
    echo "✓ 腾讯视频上传完成"
else
    echo "✗ 腾讯视频上传失败"
fi

echo "上传到小红书..."
if python upload_video_to_xiaohongshu.py; then
    echo "✓ 小红书上传完成"
else
    echo "✗ 小红书上传失败"
fi

echo "上传到B站..."
if python upload_video_to_bilibili.py; then
    echo "✓ B站上传完成"
else
    echo "✗ B站上传失败"
fi

echo ""
echo "=== 脚本执行完成 ==="
echo "结束时间: $(date)"


