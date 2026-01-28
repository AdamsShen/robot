#!/bin/bash
# GitHub 认证设置脚本

echo "================================================"
echo "  GitHub 推送认证设置"
echo "================================================"
echo ""

# 1. 清除旧凭据
echo "步骤 1: 清除旧凭据..."
rm -f ~/.git-credentials
echo "✅ 旧凭据已清除"
echo ""

# 2. 修复权限
echo "步骤 2: 修复配置文件权限..."
if [ -f ~/.gitconfig ]; then
    if [ "$(stat -c %U ~/.gitconfig)" = "root" ]; then
        echo "检测到权限问题，需要修复..."
        sudo chown $USER:$USER ~/.gitconfig && echo "✅ 权限已修复" || echo "❌ 权限修复失败，请手动执行: sudo chown $USER:$USER ~/.gitconfig"
    else
        echo "✅ 权限正常"
    fi
fi
echo ""

# 3. 配置凭据助手
echo "步骤 3: 配置 Git 凭据存储..."
git config --global credential.helper store
echo "✅ 已配置凭据存储"
echo ""

# 4. 检查配置
echo "步骤 4: 检查当前配置..."
echo "用户名: $(git config user.name)"
echo "邮箱: $(git config user.email)"
echo "远程仓库: $(cd /home/adams/robot && git remote get-url origin)"
echo ""

echo "================================================"
echo "  接下来请按照以下步骤操作："
echo "================================================"
echo ""
echo "1️⃣  在浏览器中打开以下链接："
echo "   👉 https://github.com/settings/tokens/new"
echo ""
echo "2️⃣  填写 Token 信息："
echo "   - Note: robot-wsl-access"
echo "   - Expiration: 90 days"
echo "   - ✅ 勾选 'repo' (完整的仓库控制权限)"
echo ""
echo "3️⃣  点击底部绿色按钮 'Generate token'"
echo ""
echo "4️⃣  复制生成的 token (格式: ghp_xxxxx...)"
echo ""
echo "5️⃣  执行推送命令:"
echo "   cd /home/adams/robot"
echo "   git push -u origin master"
echo ""
echo "6️⃣  当提示输入密码时，粘贴您的 token"
echo ""
echo "================================================"
echo ""
