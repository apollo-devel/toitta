<template>
    <div class="uk-margin-right">
        <div class="uk-flex uk-flex-top">
            <img :src="url" class="uk-border-circle avatar">
            <div class="uk-flex uk-flex-left uk-flex-column uk-margin-left uk-flex-1">
                <div class="uk-flex uk-flex-middle uk-flex-row">
                    <span class="uk-text-bold">{{ post.posted_by.display_name }}</span>
                    <span class="uk-margin-small-left uk-text-muted">@{{ post.posted_by.username }}</span>
                    <span class="uk-margin-small-left uk-text-muted">{{ post.created_at }}</span>
                    <span class="uk-flex-1"></span>
                    <span uk-icon="icon: close; ratio: 0.8"></span>
                </div>
                <div class="uk-flex uk-margin-small-top">
                    {{ post.content }}
                </div>
                <div class="uk-flex uk-flex-between uk-margin-small-top">
                    <span class="uk-flex-1" uk-icon="comment"></span>
                    <span class="uk-flex-1" uk-icon="bolt"></span>
                    <span class="uk-flex-1" uk-icon="heart" @click="onLikeClick"></span>
                </div>
            </div>
        </div>
        <hr>
    </div>
</template>

<script>
import { imageUrl } from '@/functions/avatar.js';
import { useStore } from 'vuex';

export default {
    props: {
        post: Object
    },
    setup(props) {
        const store = useStore();

        const url = imageUrl(props.post.posted_by);

        const onLikeClick = () => {
            store.dispatch('likePost', props.post);
        };
        return {
            url,
            onLikeClick
        };
    },
}
</script>

<style scoped>
.avatar {
    width: 50px;
    height: 50px;
}
</style>