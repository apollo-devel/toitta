<template>
    <ul class="uk-iconnav uk-iconnav-vertical uk-padding">
        <li><router-link to="/" uk-icon="icon: home; ratio: 2" uk-tooltip="title: ホーム; pos: right"></router-link></li>
        <li><router-link to="/" uk-icon="icon: search; ratio: 2" uk-tooltip="title: 検索; pos: right"></router-link></li>
        <li><router-link to="/about" uk-icon="icon: bell; ratio: 2" uk-tooltip="title: 通知; pos: right"></router-link></li>
        <li><router-link to="/" uk-icon="icon: mail; ratio: 2" uk-tooltip="title: メッセージ; pos: right"></router-link></li>
        <li><router-link to="/" uk-icon="icon: user; ratio: 2" uk-tooltip="title: プロフィール; pos: right"></router-link></li>
        <li><span @click="logout" uk-icon="icon: sign-out; ratio: 2" uk-tooltip="title: ログアウト; pos: right"></span></li>
    </ul>
</template>

<script>
import { useStore } from 'vuex';

export default {
    setup() {
        const store = useStore();

        const logout = () => {
            store.dispatch("logout");
        };

        return {
            logout
        };
    },
}
</script>
