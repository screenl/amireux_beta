<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { ref, watch } from "vue";
import Greet from "./components/Greet.vue";
import Report from "./components/Report.vue";
import TopNav from "./components/TopNav.vue";
import Signin from "./components/Signin.vue";
import Match from "./components/Match.vue";
const show = ref(-2);

</script>

<template>
    <div v-if="show==-1" >
      <Signin @signed="show=1" />
    </div>

    <img v-if="show==-2" @animationend="show=-1" id="svs" src="./assets/start.gif">
    <TopNav @goToMatch="show=2" @goToChat="show=1" @goToAnalysis="show=0" v-if="show!=-1 && show!=-2"/>

    <div v-if="show==1">
      <Greet />
    </div>
    <div v-if="show==0">
      <Report />
    </div>
    <div v-if="show==2">
      <Match />
    </div>
    

</template>

<style scoped>
.logo.vite:hover {
  filter: drop-shadow(0 0 2em #747bff);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #249b73);
}
</style>
