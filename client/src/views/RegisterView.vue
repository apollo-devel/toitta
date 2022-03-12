<template>
    <div class="uk-container">
        <h1>ユーザー登録</h1>

        <form class="uk-form-horizontal uk-margin-large" @submit.prevent>
            <div class="uk-margin">
                <label class="uk-form-label" for="register__display-name">表示名</label>
                <div class="uk-form-controls">
                    <input 
                        class="uk-input" 
                        id="register__display-name"
                        type="text"
                        v-model="displayName"
                        required>
                </div>
            </div>
            <div class="uk-margin">
                <label class="uk-form-label" for="register__username">ユーザーID</label>
                <div class="uk-form-controls">
                    <input 
                        class="uk-input"
                        id="register__username"
                        type="text"
                        v-model="username"
                        required>
                </div>
            </div>
            <div class="uk-margin">
                <label class="uk-form-label" for="register__email">メールアドレス</label>
                <div class="uk-form-controls">
                    <input 
                        class="uk-input"
                        id="register__email"
                        type="email"
                        v-model="email"
                        required>
                </div>
            </div>
            <div class="uk-margin">
                <label class="uk-form-label" for="register__password">パスワード</label>
                <div class="uk-form-controls">
                    <input 
                        class="uk-input"
                        id="register__password"
                        type="password"
                        v-model="password"
                        required>
                </div>
            </div>
            <div class="uk-margin">
                <label class="uk-form-label" for="register__password-confirm">パスワード(再確認)</label>
                <div class="uk-form-controls">
                    <input 
                        class="uk-input"
                        id="register__password-confirm"
                        type="password"
                        v-model="passwordConfirm"
                        required>
                </div>
            </div>
            <div class="uk-margin">
                <input class="uk-button uk-button-primary" type="submit"  value="登録" @click="onClick">
            </div>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';

export default {
    setup() {
        const store = useStore();

        const displayName = ref("");
        const username = ref("");
        const password = ref("");
        const passwordConfirm = ref("");
        const email = ref("");
        const onClick = () => {
            var user = {
                display_name: displayName.value,
                username: username.value,
                password: password.value,
                email: email.value
            };

            store.dispatch('registerUser', user);
        };
        return {
            displayName,
            username,
            password,
            passwordConfirm,
            email,
            onClick
        };
    },
}
</script>
