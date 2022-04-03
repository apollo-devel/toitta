<template>
  <div class="message uk-flex" :class="{ mine: isMine, theirs: !isMine }">
    <div class="image">
      <img v-if="!isMine && isLast" :src="imageUrl" />
    </div>
    <div class="container uk-flex uk-flex-column">
      <span
        class="sender uk-text-muted uk-text-small"
        v-if="!isMine && isFirst"
      >
        {{ message.sender.display_name }}
      </span>
      <span class="body uk-text-small">
        {{ message.content }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: Object,
    isMine: Boolean,
    isFirst: Boolean,
    isLast: Boolean,
  },
  setup(props) {
    const imageUrl = ((user) => {
      if (!user || !user.display_name) {
        return "https://ui-avatars.com/api/?name=?";
      }

      if (!user.profile_pic) {
        return `https://ui-avatars.com/api/?name=${user.display_name}`;
      }
      return user.profile_pic;
    })(props.message.sender);
    return {
      imageUrl,
    };
  },
};
</script>

<style scoped>
.message {
  align-items: flex-end;
  padding-bottom: 4px;
}

.message.mine {
  flex-direction: row-reverse;
}

.container {
  max-width: 55%;
}

.body {
  background-color: #f1f0f0;
  padding: 6px 12px;
  border-radius: 18px;
}

.mine .body {
  background-color: #1fa2f1;
  color: white;
}

.image {
  height: 24px;
  width: 24px;
  margin-right: 7px;
}

.image img {
  height: 100%;
  border-radius: 50%;
  vertical-align: bottom;
}
</style>