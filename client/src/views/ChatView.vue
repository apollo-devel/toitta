<template>
  <div class="uk-margin-right uk-flex uk-flex-column uk-height-1-1">
    <div>
      <h3 class="uk-margin-top">チャット</h3>
    </div>
    <div class="uk-text-bold">チャットのタイトル</div>
    <hr class="top-hr" />
    <div class="uk-flex-1 uk-flex uk-flex-column content">
      <div class="message mine uk-flex">
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="sender uk-text-muted uk-text-small">hoge</span>
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image">
          <img src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>

      <div class="message mine uk-flex">
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="sender uk-text-muted uk-text-small">hoge</span>
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image">
          <img src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>

      <div class="message mine uk-flex">
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="sender uk-text-muted uk-text-small">hoge</span>
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image">
          <img src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>

      <div class="message mine uk-flex">
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="sender uk-text-muted uk-text-small">hoge</span>
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image">
          <img src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="sender uk-text-muted uk-text-small">hoge</span>
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image"></div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
      <div class="message theirs uk-flex">
        <div class="image">
          <img src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="container uk-flex uk-flex-column">
          <span class="body uk-text-small">
            hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi hi
          </span>
        </div>
      </div>
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
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    const route = useRoute();

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

    return {
      text,
      enableSubmit,
      submit,
      onSendClick,
      isValid,
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

.clickable {
  cursor: pointer;
}
</style>