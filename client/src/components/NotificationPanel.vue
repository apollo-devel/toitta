<template>
  <div
    class="uk-flex uk-flex-row uk-flex-middle uk-margin-bottom panel"
    :class="{ active: !notification.opened }"
    @click="onClick"
  >
    <avatar-pic :user="notification.user_from" @click.stop></avatar-pic>
    <span class="uk-margin-left">{{ text }}</span>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import AvatarPic from "@/components/AvatarPic.vue";

export default {
  components: {
    AvatarPic,
  },
  props: {
    notification: Object,
  },
  setup(props) {
    const to = (() => {
      switch (props.notification.notification_type) {
        case "like":
        case "retweet":
        case "reply":
          return `/posts/${props.notification.params.post_id}`;
        case "follow":
          return `/profile/${props.notification.user_from._id}`;
      }
    })();

    const router = useRouter();

    const onClick = () => {
      router.push(to);
    };

    const text = (() => {
      const dispName = props.notification.user_from.display_name;
      switch (props.notification.notification_type) {
        case "like":
          return `${dispName} さんがあなたの投稿をいいねしました`;
        case "retweet":
          return `${dispName} さんがあなたの投稿をリツイートしました`;
        case "reply":
          return `${dispName} さんがあなたの投稿に返信しました`;
        case "follow":
          return `${dispName} さんがあなたをフォローしました`;
      }
    })();

    return {
      onClick,
      text,
    };
  },
};
</script>

<style scoped>
.panel {
  cursor: pointer;
}

.active {
  font-weight: bold;
}
</style>