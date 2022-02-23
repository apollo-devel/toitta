<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>メッセージ : {{ message }}</p>
    <p>カウント : {{ count }}</p>
    <button @click=onClick>push</button>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  setup () {
    const message = ref('');
    const count = ref(0);
    const onClick = () => {
      axios.get('/api/hello')
        .then(res => {
          message.value = res.data.message;
          count.value = res.data.count;
        });
    };
    return {
      message,
      count,
      onClick
    };
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
