<template>
  <div>
    <h3 class="uk-margin-top">通知</h3>
    <div>
      <notification-panel
        v-for="n in notifications"
        :key="n._id"
        :notification="n"
      >
      </notification-panel>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";

import NotificationPanel from "../components/NotificationPanel.vue";

export default {
  components: { NotificationPanel },
  setup() {
    const store = useStore();
    const notifications = computed(() => store.state.notifications);

    onMounted(() => {
      store.dispatch("loadNotifications");
    });
    return {
      notifications,
    };
  },
};
</script>
