<template>
    <div class="uk-container uk-width-1-2">
        <h1>Toitta Login</h1>

        <form class="uk-form-horizontal uk-margin-large" @submit.prevent>
            <div class="uk-margin">
                <label class="uk-form-label" for="login__email">メールアドレス</label>
                <div class="uk-form-controls">
                    <input
                        class="uk-input"
                        id="login__email"
                        type="text"
                        v-model="email"
                        required>
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
                        required>
                </div>
            </div> 
            <div class="uk-margin">
                <input class="uk-button uk-button-primary" type="submit"  value="ログイン" @click="onClick">
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

        const email = ref("");
        const password = ref("");
        const onClick = () => {
            const credential = {
                email: email.value,
                password: password.value
            };

            store.dispatch('login', credential);
        };
        return {
            email,
            password,
            onClick
        };
    }
}
</script>