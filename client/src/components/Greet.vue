<script setup>
import { ref } from "vue";
import { invoke } from "@tauri-apps/api/primitives";

import VueLetterAvatar from 'vue-letter-avatar';
 

const greetMsg = ref("");
const msgs = ref([]);
const name = ref("");
var loading = false;

async function greet() {
  loading = true;
  msgs.value.push({origin:1, content: name.value});
  
  let g = await invoke("greet", { name: name.value });
  greetMsg.value = g;
  msgs.value.push({origin:0, content: g}); 
  name.value = '';
  loading=false;
}

function scroll_to_bottom(){
  const elem = document.getElementById('messageDisplay');
  elem.scrollTop = elem.scrollHeight;
}
</script>

<template>
    
    <div class="imessage" id='messageDisplay'>

      <div class="start_hint">Welcome to Amireux! Before your journey starts, let's learn more about each other! What about starting from an interesting childhood memory?</div>
      <div v-for="g in msgs">
        <div v-if="g.origin==0" class="msg_flow_l">
          <img src="../assets/robot.png" class="avatar_l"> 
          <p class="from-them" @animationstart="scroll_to_bottom">{{ g.content }}</p>
        </div>
        <div v-else class="msg_flow_r">
          <p class="from-me" @animationstart="scroll_to_bottom">{{ g.content }}</p>
          <img src="../assets/dog.jpg" class="avatar_r"> 
        </div>
      </div>

    <div class="msg_flow_l" id="loading" v-show="loading">
      <img src="../assets/robot.png" class="avatar_l"> 
      <p class="from-them" @animationstart="scroll_to_bottom">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div></p>
      </div>
    </div>
  <form class="row" @submit.prevent="greet">
    <input id="greet-input" v-model="name" placeholder="Have Something to Say..." />
    <button type="submit">⇧</button>
  </form>

  <p>{{ greetMsg }}</p>
</template>
