<template>
  <div>
    <simple-post-panel
      :post="post"
      :disableLink="disableLink"
      :main="main"
      @clickReply="onReplyClick"
    ></simple-post-panel>
    <div ref="replyModal" uk-modal>
      <reply-modal
        @replySuccess="onReplySuccess"
        @closeModal="closeModal"
      ></reply-modal>
    </div>
  </div>
</template>

<script>
import UIkit from "uikit";
import { ref } from "vue";
import { useStore } from "vuex";

import ReplyModal from "@/components/ReplyModal.vue";
import SimplePostPanel from "@/components/SimplePostPanel.vue";

export default {
  components: {
    ReplyModal,
    SimplePostPanel,
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
    const replyModal = ref(null);
    const onReplyClick = () => {
      store.dispatch("openReplyModal", { post: props.post }).then(() => {
        UIkit.modal(replyModal.value).show();
      });
    };
    const onReplySuccess = () => {
      context.emit("replySuccess");
    };
    const closeModal = () => {
      UIkit.modal(replyModal.value).hide();
    };
    return {
      replyModal,
      onReplyClick,
      onReplySuccess,
      closeModal,
    };
  },
};
</script>
