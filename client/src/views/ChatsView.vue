<template>
  <div class="uk-margin-right">
    <div class="uk-flex uk-flex-row uk-flex-middle">
      <h3 class="uk-margin-top">メッセージ</h3>
      <span class="uk-flex-1"></span>
      <span uk-icon="plus" class="clickable" @click="onNewClick"></span>
    </div>
    <div>
      <div
        v-for="chat in chats"
        :key="chat._id"
        @click="onChatClick(chat)"
        class="clickable"
      >
        <div class="uk-flex uk-flex-row uk-flex-middle">
          <div
            class="image-container uk-position-relative uk-margin-small-right uk-flex uk-flex-center multi"
            v-if="isMulti(chat)"
          >
            <img
              class="avatar uk-position-absolute"
              :src="getUserImage(chat, 0)"
            />
            <img
              class="avatar uk-position-absolute"
              :src="getUserImage(chat, 1)"
            />
          </div>
          <div
            class="image-container uk-position-relative uk-margin-small-right uk-flex uk-flex-center"
            v-else
          >
            <img class="avatar" :src="getUserImage(chat, 0)" />
          </div>
          <div class="uk-flex-1 uk-flex uk-flex-column uk-width-expand">
            <div class="uk-text-bold uk-text-truncate uk-margin-right">
              {{ chatName(chat) }}
            </div>
            <div
              class="uk-text-small uk-text-muted uk-text-truncate uk-margin-right"
            >
              {{ latestMessage(chat) }}
            </div>
          </div>
        </div>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();

    store.dispatch("loadChats");

    const chats = computed(() => store.state.chat.chats);

    const chatName = (chat) => {
      if (chat.name) {
        return chat.name;
      }
      return chat.users
        .filter((u) => u._id !== store.state.userLoggedIn._id)
        .map((u) => u.display_name)
        .join(", ");
    };

    const latestMessage = (chat) => {
      if (chat.latestMessage) {
        return chat.latestMessage;
      }
      return "(まだメッセージがありません)";
    };

    const isMulti = (chat) => {
      return chat.users.length > 2;
    };

    const imageUrl = (user) => {
      if (!user || !user.display_name) {
        return "https://ui-avatars.com/api/?name=?";
      }

      if (!user.profile_pic) {
        return `https://ui-avatars.com/api/?name=${user.display_name}`;
      }
      return user.profile_pic;
    };

    const getUserImage = (chat, idx) => {
      return chat.users
        .filter((u) => u._id !== store.state.userLoggedIn._id)
        .map((u) => imageUrl(u))[idx];
    };

    const router = useRouter();
    const onNewClick = () => {
      router.push({ name: "newChat" });
    };

    const onChatClick = (chat) => {
      router.push({ name: "chat", params: { chatId: chat._id } });
    };

    return {
      chats,
      chatName,
      latestMessage,
      isMulti,
      getUserImage,
      onNewClick,
      onChatClick,
    };
  },
};
</script>

<style scoped>
.image-container {
  width: 40px;
  height: 40px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid white;
}

.multi .avatar {
  height: 65%;
  width: 65%;
  bottom: 0;
  margin: 0;
}

.multi .avatar:first-of-type {
  top: 0;
  right: 0;
}

.clickable {
  cursor: pointer;
}
</style>