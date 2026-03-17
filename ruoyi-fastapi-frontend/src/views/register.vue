<template>
  <div class="register">
    <div class="auth-shell">
      <div class="auth-brand">
        <div class="auth-brand__mark">{{ title }}</div>
        <div class="auth-brand__sub">创建你的管理账号</div>
        <div class="auth-brand__chips">
          <el-tag effect="plain" size="large" class="chip">更快建档</el-tag>
          <el-tag effect="plain" size="large" class="chip">更好治理</el-tag>
          <el-tag effect="plain" size="large" class="chip">更稳运营</el-tag>
        </div>
        <div class="auth-brand__hint">
          注册成功后即可进入后台，维护软件分类、软件条目、下载配置与资源链接。
        </div>
      </div>

      <el-form
        ref="registerRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        @submit.prevent="handleRegister"
      >
        <div class="form-head">
          <div class="form-title">注册</div>
          <div class="form-sub">加入 {{ title }} 管理后台</div>
        </div>
      <el-form-item prop="username">
        <el-input 
          v-model="registerForm.username" 
          type="text" 
          size="large" 
          auto-complete="off" 
          placeholder="账号"
        >
          <template #prefix><svg-icon icon-class="user" class="el-input__icon input-icon" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="registerForm.password"
          type="password"
          size="large" 
          auto-complete="off"
          placeholder="密码"
          @keyup.enter="handleRegister"
        >
          <template #prefix><svg-icon icon-class="password" class="el-input__icon input-icon" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input
          v-model="registerForm.confirmPassword"
          type="password"
          size="large" 
          auto-complete="off"
          placeholder="确认密码"
          @keyup.enter="handleRegister"
        >
          <template #prefix><svg-icon icon-class="password" class="el-input__icon input-icon" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="code" v-if="captchaEnabled">
        <el-input
          size="large" 
          v-model="registerForm.code"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
          @keyup.enter="handleRegister"
        >
          <template #prefix><svg-icon icon-class="validCode" class="el-input__icon input-icon" /></template>
        </el-input>
        <div class="register-code">
          <img :src="codeUrl" @click="getCode" class="register-code-img"/>
        </div>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          :loading="loading"
          size="large" 
          type="primary"
          style="width:100%;"
          native-type="submit"
          @click.prevent="handleRegister"
        >
          <span v-if="!loading">注 册</span>
          <span v-else>注 册 中...</span>
        </el-button>
        <div style="float: right;">
          <router-link class="link-type" :to="'/login'">使用已有账户登录</router-link>
        </div>
      </el-form-item>
      </el-form>
    </div>
    <!--  底部  -->
    <div class="el-register-footer">
      <span>{{ footerContent }}</span>
    </div>
  </div>
</template>

<script setup>
import { ElMessageBox } from "element-plus";
import { getCodeImg, register } from "@/api/login";
import defaultSettings from '@/settings'
import { APP_TITLE } from '@/config/brand'

const title = APP_TITLE;
const footerContent = defaultSettings.footerContent
const router = useRouter();
const { proxy } = getCurrentInstance();

const registerForm = ref({
  username: "",
  password: "",
  confirmPassword: "",
  code: "",
  uuid: ""
});

const equalToPassword = (rule, value, callback) => {
  if (registerForm.value.password !== value) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const registerRules = {
  username: [
    { required: true, trigger: "blur", message: "请输入您的账号" },
    { min: 2, max: 20, message: "用户账号长度必须介于 2 和 20 之间", trigger: "blur" }
  ],
  password: [
    { required: true, trigger: "blur", message: "请输入您的密码" },
    { min: 5, max: 20, message: "用户密码长度必须介于 5 和 20 之间", trigger: "blur" },
    { pattern: /^[^<>"'|\\]+$/, message: "不能包含非法字符：< > \" ' \\\ |", trigger: "blur" }
  ],
  confirmPassword: [
    { required: true, trigger: "blur", message: "请再次输入您的密码" },
    { required: true, validator: equalToPassword, trigger: "blur" }
  ],
  code: [{ required: true, trigger: "change", message: "请输入验证码" }]
};

const codeUrl = ref("");
const loading = ref(false);
const captchaEnabled = ref(true);

function handleRegister() {
  proxy.$refs.registerRef.validate(valid => {
    if (valid) {
      loading.value = true;
      register(registerForm.value).then(res => {
        const username = registerForm.value.username;
        ElMessageBox.alert("<font color='red'>恭喜你，您的账号 " + username + " 注册成功！</font>", "系统提示", {
          dangerouslyUseHTMLString: true,
          type: "success",
        }).then(() => {
          router.push("/login");
        }).catch(() => {});
      }).catch(() => {
        loading.value = false;
        if (captchaEnabled) {
          getCode();
        }
      });
    }
  });
}

function getCode() {
  getCodeImg().then(res => {
    captchaEnabled.value = res.captchaEnabled === undefined ? true : res.captchaEnabled;
    if (captchaEnabled.value) {
      codeUrl.value = "data:image/gif;base64," + res.img;
      registerForm.value.uuid = res.uuid;
    }
  });
}

getCode();
</script>

<style lang='scss' scoped>
.register {
  min-height: 100vh;
  padding: 28px 18px 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(900px circle at 14% 16%, rgba(14, 165, 233, 0.22), transparent 55%),
    radial-gradient(860px circle at 84% 22%, rgba(48, 176, 143, 0.18), transparent 55%),
    radial-gradient(900px circle at 44% 86%, rgba(254, 193, 113, 0.16), transparent 60%),
    linear-gradient(180deg, rgba(246, 247, 251, 0.82), rgba(246, 247, 251, 0.92)),
    url("../assets/images/login-background.jpg");
  background-size: cover;
  background-position: center;
}

html.dark .register {
  background:
    radial-gradient(900px circle at 14% 16%, rgba(14, 165, 233, 0.20), transparent 55%),
    radial-gradient(860px circle at 84% 22%, rgba(48, 176, 143, 0.18), transparent 55%),
    radial-gradient(900px circle at 44% 86%, rgba(254, 193, 113, 0.14), transparent 60%),
    linear-gradient(180deg, rgba(7, 10, 16, 0.84), rgba(7, 10, 16, 0.94)),
    url("../assets/images/login-background.jpg");
  background-size: cover;
  background-position: center;
}

.register:before {
  content: "";
  position: absolute;
  inset: -2px;
  pointer-events: none;
  background-image:
    repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.06) 1px, transparent 1px, transparent 3px),
    repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.04) 1px, transparent 1px, transparent 3px);
  opacity: 0.32;
  mix-blend-mode: overlay;
}

.auth-shell {
  width: min(980px, 100%);
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
  align-items: stretch;
  position: relative;
  z-index: 1;
}

@media (max-width: 920px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }
}

.auth-brand {
  border-radius: 18px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface-2) 70%, transparent);
  box-shadow: var(--app-shadow);
  padding: 20px 18px 18px;
  overflow: hidden;
  position: relative;

  @supports ((-webkit-backdrop-filter: blur(10px)) or (backdrop-filter: blur(10px))) {
    -webkit-backdrop-filter: blur(10px) saturate(1.15);
    backdrop-filter: blur(10px) saturate(1.15);
  }
}

.auth-brand__mark {
  font-size: 22px;
  font-weight: 850;
  letter-spacing: -0.02em;
  color: var(--el-text-color-primary);
}

.auth-brand__sub {
  margin-top: 6px;
  color: var(--el-text-color-secondary);
  font-weight: 600;
}

.auth-brand__chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border-radius: 999px;
  font-weight: 650;
}

.auth-brand__hint {
  margin-top: 12px;
  color: var(--el-text-color-regular);
  line-height: 20px;
}

.register-form {
  border-radius: 18px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  box-shadow: var(--app-shadow);
  padding: 18px 18px 6px;
  .el-input {
    height: 40px;
    input {
      height: 40px;
    }
  }
  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 0px;
  }
}

html.dark .register-form {
  background: var(--el-bg-color);
}

.form-head {
  margin-bottom: 14px;
}

.form-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--el-text-color-primary);
}

.form-sub {
  margin-top: 4px;
  color: var(--el-text-color-secondary);
}

.register-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}
.register-code {
  width: 33%;
  height: 40px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}
.el-register-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: var(--app-font-sans);
  font-size: 12px;
  letter-spacing: 1px;
  opacity: 0.88;
}
.register-code-img {
  height: 40px;
  padding-left: 12px;
}
</style>
