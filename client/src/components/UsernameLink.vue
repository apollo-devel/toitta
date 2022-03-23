<template>
  <span class="uk-text-muted">
    <router-link :to="'/profile/' + user.username" class="uk-link-text">
      @{{ user.username }}
    </router-link>
  </span>
</template>

<script>
export default {
  props: {
    user: Object,
  },
};
</script>
