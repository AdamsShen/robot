# GitHub 推送指南

## ⚠️ 重要提示
GitHub 不再支持密码认证！必须使用 Personal Access Token (PAT)

## 🔑 获取 GitHub Personal Access Token

### 步骤 1：生成 Token
1. 打开浏览器访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** 按钮
3. 选择 **"Generate new token (classic)"**
4. 填写表单：
   - **Note**: 输入 `robot-wsl-token`（随便起个名字）
   - **Expiration**: 选择 `90 days` 或更长
   - **Select scopes**: ✅ **必须勾选 `repo`** (完整仓库访问权限)
5. 滚动到页面底部，点击绿色的 **"Generate token"** 按钮
6. **立即复制显示的 token！**（格式：`ghp_xxxxxxxxxxxxxxxxxxxxxxxx`）
   - ⚠️ Token 只显示一次，关闭页面后无法再次查看

### 步骤 2：修复文件权限（如果需要）
```bash
sudo chown adams:adams ~/.gitconfig
```

### 步骤 3：配置 Git 保存凭据
```bash
git config --global credential.helper store
```

### 步骤 4：推送代码
```bash
cd /home/adams/robot
git push -u origin master
```

**当提示输入密码时：**
- Username: 直接按回车（已包含在 URL 中）
- Password: **粘贴您的 Personal Access Token**（不是 GitHub 密码！）

## ✅ 验证
推送成功后，访问：https://github.com/AdamsShen/robot
应该能看到您的代码了！

## ❌ 常见错误
1. **"Invalid username or token"** 
   - 您输入的可能是 GitHub 密码，不是 token
   - 或者 token 没有勾选 `repo` 权限
   - 或者 token 已过期

2. **"Password authentication is not supported"**
   - 不能使用密码，必须使用 token

3. **Token 格式**
   - ✅ 正确：`ghp_xxxxxxxxxxxxxxxxxxxx` (以 ghp_ 开头)
   - ❌ 错误：输入了 GitHub 账号密码
