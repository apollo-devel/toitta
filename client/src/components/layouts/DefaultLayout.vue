<template>
  <div class="uk-grid">
    <div class="uk-width-auto">
      <side-nav></side-nav>
    </div>
    <div class="uk-width-expand">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  components: {
    SideNav,
  },
};
</script>
