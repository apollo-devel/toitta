<template>
  <div class="uk-container uk-width-1-2 uk-text-center uk-padding">
    <h1>Toitta Login</h1>

    <form class="uk-form-horizontal uk-margin-large" @submit="onSubmit">
      <div class="uk-margin">
        <label class="uk-form-label" for="login__identifier"
          >ユーザー名 または メールアドレス</label
        >
        <div class="uk-form-controls">
          <input
            class="uk-input"
            id="login__identifier"
            type="text"
            v-model="identifier"
            required
          />
        </div>
      </div>
      <div class="uk-margin">
        <label class="uk-form-label" for="login__password">パスワード</label>
        <div class="uk-form-controls">
          <input
            class="uk-input"
            id="login__password"
            type="password"
            v-model="password"
            required
          />
        </div>
      </div>
      <div class="uk-margin">
        <input
          class="uk-button uk-button-primary"
          type="submit"
          value="ログイン"
        />
      </div>
    </form>
    <div>
      アカウントがない場合は
      <router-link to="/register">アカウント登録</router-link>
      してください
    </div>
  </div>
</template>

<script>
import UIkit from "uikit";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const identifier = ref("");
    const password = ref("");
    const onSubmit = (e) => {
      e.preventDefault();

      const credential = {
        identifier: identifier.value,
        password: password.value,
      };

      store
        .dispatch("login", { credential })
        .then(() => router.push("/"))
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    };
    return {
      identifier,
      password,
      onSubmit,
    };
  },
};
</script>