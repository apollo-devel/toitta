<template>
  <div class="uk-margin-right">
    <div class="uk-margin-small-left uk-margin-small-bottom" v-if="isRetweet">
      {{ post.posted_by.display_name }}がリツイート
    </div>
    <div class="uk-flex uk-flex-top">
      <img :src="url" class="uk-border-circle avatar" />
      <div class="uk-flex uk-flex-left uk-flex-column uk-margin-left uk-flex-1">
        <div class="uk-flex uk-flex-middle uk-flex-row">
          <span class="uk-text-bold">{{
            displayPost.posted_by.display_name
          }}</span>
          <span class="uk-margin-small-left uk-text-muted"
            >@{{ displayPost.posted_by.username }}</span
          >
          <span class="uk-margin-small-left uk-text-muted">{{
            displayPost.created_at
          }}</span>
          <span class="uk-flex-1"></span>
          <span uk-icon="icon: close; ratio: 0.8"></span>
        </div>
        <div class="uk-flex uk-margin-small-top">
          {{ displayPost.content }}
        </div>
        <div class="uk-flex uk-flex-between uk-margin-small-top">
          <span class="uk-flex-1" uk-icon="comment"></span>
          <span
            class="uk-flex-1 retweet"
            :class="{ active: displayPost.retweeting }"
          >
            <span uk-icon="bolt" @click="onRetweetClick"></span>
            <span class="uk-margin-small-left">{{
              displayPost.retweet_count ? displayPost.retweet_count : ""
            }}</span>
          </span>
          <span class="uk-flex-1 like" :class="{ active: displayPost.liking }">
            <span uk-icon="heart" @click="onLikeClick"></span>
            <span class="uk-margin-small-left">{{
              displayPost.like_count ? displayPost.like_count : ""
            }}</span>
          </span>
        </div>
      </div>
    </div>
    <hr />
  </div>
</template>

<script>
import { useStore } from "vuex";

import { imageUrl } from "@/functions/avatar.js";

export default {
  props: {
    post: Object,
  },
  setup(props) {
    const store = useStore();

    const isRetweet = Boolean(props.post.retweeted_post);
    const displayPost = isRetweet ? props.post.retweeted_post : props.post;

    const url = imageUrl(displayPost.posted_by);

    const onLikeClick = () => {
      if (displayPost.liking) {
        store.dispatch("unlikePost", { post: displayPost });
      } else {
        store.dispatch("likePost", { post: displayPost });
      }
    };

    const onRetweetClick = () => {
      if (displayPost.retweeting) {
        store.dispatch("unretweetPost", { post: displayPost });
      } else {
        store.dispatch("retweetPost", { post: displayPost });
      }
    };
    return {
      isRetweet,
      displayPost,
      url,
      onLikeClick,
      onRetweetClick,
    };
  },
};
</script>

<style scoped>
.avatar {
  width: 50px;
  height: 50px;
}

.like.active {
  color: red;
}

.retweet.active {
  color: green;
}

.like,
.retweet {
  cursor: pointer;
}
</style>