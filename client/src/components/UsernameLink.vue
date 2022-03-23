<template>
  <span class="uk-text-muted">
    <router-link
      :to="'/profile/' + user.username"
      class="uk-link-text"
      v-if="!disableLink"
    >
      @{{ user.username }}
    </router-link>
    <span v-else>@{{ user.username }}</span>
  </span>
</template>

<script>
export default {
  props: {
    user: Object,
    disableLink: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
