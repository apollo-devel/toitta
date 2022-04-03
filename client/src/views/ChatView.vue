<template>
  <div class="uk-margin-right uk-flex uk-flex-column uk-height-1-1">
    <div>
      <h3 class="uk-margin-top">チャット</h3>
    </div>
    <div class="uk-text-bold">
      {{ chatName(chat, userLoggedIn) }}
    </div>
    <div class="uk-margin-small-top">
      <avatar-pic
        v-for="user in users"
        :key="user._id"
        :user="user"
        size="small"
        :disableLink="true"
        class="uk-margin-small-right"
      ></avatar-pic>
    </div>
    <hr class="top-hr" />
    <div class="uk-flex-1 uk-flex uk-flex-column content">
      <chat-message
        v-for="(message, idx) in messages"
        :key="message._id"
        :message="message"
        :isMine="isMine(message)"
        :isFirst="isFirst(message, idx)"
        :isLast="isLast(message, idx)"
      ></chat-message>
    </div>
    <hr class="bottom-hr" />
    <div class="uk-flex uk-flex-row uk-flex-middle uk-margin-bottom">
      <input
        type="text"
        class="uk-input uk-flex-1 uk-margin-right"
        v-model="text"
        @keypress.prevent.enter.exact="enableSubmit"
        @keyup.prevent.enter.exact="submit"
      />
      <span
        uk-icon="icon: comment; ratio: 1.5"
        @click="onSendClick"
        :class="{ clickable: isValid }"
        :disabled="!isValid"
      ></span>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";
import ChatMessage from "@/components/ChatMessage.vue";
import { chatName } from "@/functions/chat.js";

export default {
  components: {
    ChatMessage,
    AvatarPic,
  },
  setup() {
    const store = useStore();
    const route = useRoute();

    const userLoggedIn = store.state.userLoggedIn;

    const text = ref("");

    const canSubmit = ref(false);

    const enableSubmit = () => {
      canSubmit.value = true;
    };

    const _post = () => {
      store
        .dispatch("sendMessage", {
          content: text.value,
          sender: store.state.userLoggedIn._id,
          chat: route.params["chatId"],
        })
        .then(() => (text.value = ""));
    };

    const submit = () => {
      if (!canSubmit.value || !text.value.trim()) {
        return;
      }
      _post();
      canSubmit.value = false;
    };

    const onSendClick = () => {
      if (!text.value.trim()) {
        return;
      }
      _post();
      canSubmit.value = false;
    };

    const isValid = computed(() => {
      return Boolean(text.value);
    });

    watch(
      () => route.params,
      (newParams) => {
        store.dispatch("loadChat", { chat: newParams["chatId"] });
        store.dispatch("loadMessages", { chat: newParams["chatId"] });
      },
      {
        immediate: true,
      }
    );

    const messages = computed(() => store.state.chat.messages);

    const isMine = (message) => {
      return message.sender._id === store.state.userLoggedIn._id;
    };

    const isFirst = (message, idx) => {
      if (idx === 0) {
        return true;
      }
      const prev = messages.value[idx - 1];
      return prev.sender._id != message.sender._id;
    };

    const isLast = (message, idx) => {
      if (idx === messages.value.length - 1) {
        return true;
      }
      const next = messages.value[idx + 1];
      return next.sender._id != message.sender._id;
    };

    const chat = computed(() => store.state.chat.chat);
    const users = computed(() => {
      return store.state.chat.chat.users.filter(
        (u) => u._id != store.state.userLoggedIn._id
      );
    });

    return {
      userLoggedIn,
      messages,
      text,
      enableSubmit,
      submit,
      onSendClick,
      isValid,
      isMine,
      isFirst,
      isLast,
      chatName,
      chat,
      users,
    };
  },
};
</script>

<style scoped>
.content {
  overflow-y: auto;
  margin: 0;
  padding: 5px;
}

.top-hr {
  margin-bottom: 0;
}

.bottom-hr {
  margin-top: 0;
}

.clickable {
  cursor: pointer;
}
</style>