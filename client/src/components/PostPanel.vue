<template>
  <div
    class="uk-margin-right"
    :class="{ clickable: !disableLink }"
    @click="onBodyClick"
  >
    <div class="uk-margin-small-left uk-margin-small-bottom" v-if="isRetweet">
      <router-link
        @click.stop
        :to="'/profile/' + post.posted_by.username"
        class="uk-link-text"
      >
        {{ post.posted_by.display_name }}がリツイート
      </router-link>
    </div>
    <div class="uk-flex uk-flex-top">
      <avatar-pic
        @click.stop
        :user="displayPost.posted_by"
        :disableLink="disableLink"
      ></avatar-pic>
      <div class="uk-flex uk-flex-left uk-flex-column uk-margin-left uk-flex-1">
        <div class="uk-flex uk-flex-middle uk-flex-row">
          <display-name
            @click.stop
            :user="displayPost.posted_by"
            :disableLink="disableLink"
          ></display-name>
          <username-link
            @click.stop
            :user="displayPost.posted_by"
            :disableLink="disableLink"
            class="uk-margin-small-left"
          ></username-link>
          <span class="uk-margin-small-left uk-text-muted">
            {{ displayPost.created_at }}
          </span>
          <span class="uk-flex-1"></span>
          <!-- 削除ボタン -->
          <span
            v-if="isOwnPost && !disableLink"
            uk-icon="icon: close; ratio: 0.8"
            @click.stop="onDeleteClick"
          ></span>
        </div>
        <div v-if="isReply && !disableLink">
          <router-link
            @click.stop
            :to="
              displayPost.reply_to
                ? '/profile/' + displayPost.reply_to.posted_by.username
                : ''
            "
          >
            @{{
              displayPost.reply_to
                ? displayPost.reply_to.posted_by.username
                : ""
            }}
          </router-link>
          へ返信
        </div>
        <div
          class="uk-flex uk-margin-small-top"
          :class="{ 'uk-text-large': main }"
        >
          {{ displayPost.content }}
        </div>
        <div
          class="uk-flex uk-flex-between uk-margin-small-top"
          v-if="!disableLink"
        >
          <!-- 返信 -->
          <span class="uk-flex-1 reply">
            <span uk-icon="comment" @click.stop="onReplyClick"></span>
            <span class="uk-margin-small-left">
              {{ displayPost.reply_count ? displayPost.reply_count : "" }}
            </span>
          </span>
          <!-- リツイート -->
          <span
            class="uk-flex-1 retweet"
            :class="{ active: displayPost.retweeting }"
          >
            <span uk-icon="bolt" @click.stop="onRetweetClick"></span>
            <span class="uk-margin-small-left">{{
              displayPost.retweet_count ? displayPost.retweet_count : ""
            }}</span>
          </span>
          <!-- いいね -->
          <span class="uk-flex-1 like" :class="{ active: displayPost.liking }">
            <span uk-icon="heart" @click.stop="onLikeClick"></span>
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
import UIkit from "uikit";
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";
import DisplayName from "@/components/DisplayName.vue";
import UsernameLink from "@/components/UsernameLink.vue";

export default {
  components: {
    AvatarPic,
    DisplayName,
    UsernameLink,
  },
  props: {
    post: Object,
    disableLink: Boolean,
    main: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, context) {
    const store = useStore();

    const isRetweet = computed(() =>
      Boolean(props.post && props.post.retweeted_post)
    );
    const isReply = computed(() => Boolean(props.post && props.post.reply_to));
    const displayPost = computed(() =>
      isRetweet.value ? props.post.retweeted_post : props.post
    );

    const onLikeClick = () => {
      if (displayPost.value.liking) {
        store.dispatch("unlikePost", { post: displayPost.value });
      } else {
        store.dispatch("likePost", { post: displayPost.value });
      }
    };

    const onRetweetClick = () => {
      if (displayPost.value.retweeting) {
        store.dispatch("unretweetPost", { post: displayPost.value });
      } else {
        store.dispatch("retweetPost", { post: displayPost.value });
      }
    };

    const onReplyClick = () => {
      context.emit("clickReply", displayPost.value);
    };

    const router = useRouter();
    const onBodyClick = () => {
      if (props.disableLink) {
        return;
      }
      router.push(`/posts/${displayPost.value._id}`);
    };

    const isOwnPost = computed(() => {
      return (
        displayPost.value.posted_by &&
        displayPost.value.posted_by._id === store.state.userLoggedIn._id
      );
    });

    const onDeleteClick = () => {
      UIkit.modal.confirm("ツイートを削除します。").then(
        () => {
          store.dispatch("deletePost", { postId: displayPost.value._id });
        },
        () => {
          // noop
        }
      );
    };

    return {
      isRetweet,
      isReply,
      isOwnPost,
      displayPost,
      onLikeClick,
      onRetweetClick,
      onReplyClick,
      onBodyClick,
      onDeleteClick,
    };
  },
};
</script>

<style scoped>
.like.active {
  color: red;
}

.retweet.active {
  color: green;
}

.like,
.retweet,
.reply {
  cursor: pointer;
}

.clickable {
  cursor: pointer;
}
</style>