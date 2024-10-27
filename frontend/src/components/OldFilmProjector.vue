<template>
    <div
    class="oldprojector"
    @mousedown="startDrag"
    :style="{ left: `${position.x}px`, top: `${position.y}px` }"
  >
  <div class="scene" @click="lightsOn">
    <!-- <div class="unit q"></div> -->
    <div class="detail q"></div>
    <div class="detail two q"></div>
    <div class="detail three q"></div>
    <div class="detail four q"></div>
    <div class="detail five q"></div>
    <div class="detail six q"></div>
    <div class="detail seven q"></div>
    <div class="detail eight q"></div>
    <div class="detail nine q"></div>
    <div class="detail ten q"></div>
    <div class="detail eleven q"></div>
    <div class="detail twelve q"></div>
    <div class="entry q"></div>
    <div class="entry-holder q"></div>
    <div class="top-block q"></div>
    <div class="film-roll q"></div>
    <div class="film-roll-two q"></div>
    <div class="film-roll-behind q"></div>
    <div class="film-roll-behind-two q"></div>
    <div class="film-roll-behind-three q"></div>
    <div class="film-roll-behind-four q"></div>
    <div class="film-roll-behind-five q"></div>
    <div class="film-roll-behind-six q"></div>
    <div class="film-roll-behind-seven q"></div>
    <div class="film-roll-behind-eight q"></div>
    <div class="leg"></div>
    <div class="leg-two"></div>
    <div class="shape-sq first c"></div>
    <div class="shape-ci"></div>
    <div class="shape-tri c"></div>
    <div class="shape-tri hide-one c"></div>
    <div class="shape-sq hide-two c"></div>
    <div class="shape-ci hide-three c"></div>
    <div class="shape-sq hide-four c"></div>
    <div class="shape-sq hide-five c"></div>
    <div class="shape-sq hide-six c"></div>
    <div class="shape-ci hide-seven c"></div>
    <div class="shape-ci hide-eight c"></div>
    <div class="front-block"></div>
    <div class="front-block-two"></div>
  </div>
</div>
</template>

<script>
export default {
  name: 'OldFilmProjector',
  data() {
    return {
      isDragging: false,
      position: { x: 0, y: 0 }, // 初始位置
      dragStart: { x: 0, y: 0 }
    };
  },
  methods: {
    lightsOn() {
      const light = document.querySelector('.front-block-two');
      const shapes = document.querySelectorAll('.c');

      light.classList.toggle('lights-on');
      shapes.forEach(shape => {
        if (shape.classList.contains('shape-tri')) {
          shape.classList.toggle('b');
        } else {
          shape.classList.toggle('d');
        }
      });
    },
    startDrag(event) {
      // 记录拖动开始时的鼠标位置和组件位置
      this.isDragging = true;
      this.dragStart = {
        x: event.clientX - this.position.x,
        y: event.clientY - this.position.y
      };
      // 添加鼠标移动和松开事件
      document.addEventListener('mousemove', this.onDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    onDrag(event) {
      if (this.isDragging) {
        // 计算新的位置
        this.position.x = event.clientX - this.dragStart.x;
        this.position.y = event.clientY - this.dragStart.y;
      }
    },
    stopDrag() {
      // 停止拖动并移除事件监听
      this.isDragging = false;
      document.removeEventListener('mousemove', this.onDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    }
  }
};
</script>

<style scoped>
.oldprojector {
  position: absolute; /* 需要设置为绝对定位 */
  cursor: move; /* 改变鼠标样式 */
  /* 其他样式保持不变 */
}
/* 基础样式 */
*, *::before, *::after {
  box-sizing: border-box;
}
.scene {
  --scene-h: 19;
  --scene-w: 29;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: #3B2A6F;
  width: calc(var(--scene-w) * 1vmin);
  height: calc(var(--scene-h) * 1vmin);
  z-index: 99999;
  cursor: pointer;
}
.front-block-two {
  --scene-h: 150;
  --scene-w: 150;
  position: absolute;
  border-radius: 3000px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) rotate(-90deg);
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  background: linear-gradient(to bottom, #3B2A6F 0% 6%, #0D0B40 6% 100%);
  width: calc(var(--scene-w) * 1vmin);
  height: calc(var(--scene-h) * 1vmin);
  z-index: 999;
}
.lights-on {
  background: linear-gradient(to bottom, #3B2A6F 0% 6%, rgba(249, 250, 134, .8) 6% 100%);
}
.b {
  border-bottom-color: #4A2CDE;
}
.d {
  background: #4A2CDE;
}
.c {
  background: transparent;
}
body {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            margin: 0;
            padding: 0;
            background: #0D0B40
        }

        .entry {
            --scene-h: 3.75;
            --scene-w: 2.25;
            position: relative;
            left: -7.75%;
            top: -95%;
            background-color: rgba(255, 255, 255, 75);
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 1
        }

        .entry-holder {
            --scene-h: 5.5;
            --scene-w: 2.5;
            position: relative;
            left: -14%;
            top: -119.25%;
            background: #3B2A6F;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .top-block {
            --scene-h: 8;
            --scene-w: 18;
            position: relative;
            left: 18%;
            top: -200%;
            background: #3B2A6F;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll {
            --scene-h: 15;
            --scene-w: 15;
            position: relative;
            left: -6%;
            top: -287%;
            background: #3B2A6F;
            background: #D3D6E5;
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-two {
            --scene-h: 17;
            --scene-w: 17;
            position: relative;
            left: 50%;
            top: -376%;
            background: #3B2A6F;
            background: #D3D6E5;
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind {
            --scene-h: 3.5;
            --scene-w: 3.5;
            position: relative;
            left: 14.5%;
            top: -448%;
            background: linear-gradient(to top, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-two {
            --scene-h: 3.5;
            --scene-w: 3.5;
            position: relative;
            left: 14.5%;
            top: -420%;
            background: linear-gradient(to bottom, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-three {
            --scene-h: 3.5;
            --scene-w: 3.5;
            position: relative;
            left: -1.5%;
            top: -463%;
            background: linear-gradient(to left, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-four {
            --scene-h: 3.5;
            --scene-w: 3.5;
            position: relative;
            left: 30%;
            top: -481%;
            background: linear-gradient(to right, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-five {
            --scene-h: 4.25;
            --scene-w: 4.25;
            position: relative;
            left: 91%;
            top: -504%;
            background: linear-gradient(to right, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-six {
            --scene-h: 4.25;
            --scene-w: 4.25;
            position: relative;
            left: 73%;
            top: -500%;
            background: linear-gradient(to bottom, #3B2A6F 70%, #0D0B40 70%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-seven {
            --scene-h: 4.25;
            --scene-w: 4.25;
            position: relative;
            left: 54%;
            top: -550%;
            background: linear-gradient(to left, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .film-roll-behind-eight {
            --scene-h: 4.25;
            --scene-w: 4.25;
            position: relative;
            left: 72.5%;
            top: -600%;
            background: linear-gradient(to top, #3B2A6F 60%, #0D0B40 60%);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .shape-sq {
            --scene-h: 10;
            --scene-w: 10;
            position: relative;
            left: 220%;
            top: -880%;
            transform: rotate(20deg);
            background: #5E4BBE;
            background: #4A2CDE;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 9999
        }

        .scene .lights-on {
            background: linear-gradient(to bottom, #3B2A6F 0% 6%, rgba(249, 250, 134, .8) 6% 100%)
        }

        .first {
            background: #4A2CDE;
            width: calc(var(--scene-w) / 1.5 * 1vmin);
            height: calc(var(--scene-h) / 1.5 * 1vmin)
        }

        .shape-ci {
            --scene-h: 11;
            --scene-w: 11;
            position: relative;
            left: -20%;
            top: -1100%;
            transform: rotate(35deg);
            border-radius: 50%;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 9999
        }

        .shape-tri {
            --scene-h: 10;
            --scene-w: 10;
            position: relative;
            left: 250%;
            top: -920%;
            border-right: calc(var(--scene-h) / 2 * 1vmin) solid transparent;
            border-left: calc(var(--scene-h) / 1.5 * 1vmin) solid transparent;
            border-bottom: calc(var(--scene-h) * 1vmin) solid transparent;
            transform: rotate(140deg);
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 9999
        }

        .hide-one {
            top: -930%;
            left: 303%;
            border-right: calc(var(--scene-h) * 1.1 * 1vmin) solid transparent;
            border-left: calc(var(--scene-h) / 1 * 1vmin) solid transparent;
            border-bottom: calc(var(--scene-h) * 2 * 1vmin) solid transparent;
            transform: rotate(90deg)
        }

        .hide-two {
            top: -1110%;
            left: 330%;
            width: calc(var(--scene-w) * 1.1 * 1vmin);
            height: calc(var(--scene-h) * 1.1 *1vmin)
        }

        .hide-three {
            background: #4A2CDE;
            top: -1230%;
            left: 277%
        }

        .hide-four {
            top: -1330%;
            left: 330%;
            clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
            transform: rotate(-80deg);
            width: calc(var(--scene-w) * 1.8 * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            background: #4A2CDE
        }

        .hide-five {
            top: -1250%;
            left: 170%;
            border-radius: 50%;
            background: #4A2CDE;
            transform: rotate(120deg)
        }

        .hide-six {
            top: -1250%;
            left: 215%;
            clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
            background: #4A2CDE;
            transform: rotate(55deg);
            width: calc(var(--scene-w) / 1.2 * 1vmin);
            height: calc(var(--scene-h) * 1.1 * 1vmin)
        }

        .hide-seven {
            top: -1210%;
            left: 345%;
            background: #4A2CDE
        }

        .hide-eight {
            top: -1310%;
            left: 265%;
            width: calc(var(--scene-w) / 1.8 * 1vmin);
            height: calc(var(--scene-h) / 1.8 * 1vmin);
            background: #4A2CDE
        }

        .front-block {
            --scene-h: 6;
            --scene-w: 6;
            position: relative;
            left: 100%;
            top: -1435%;
            background: #3B2A6F;
            background-color: #D3D6E5;
            background: #D3D6E5;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 9999
        }

        .front-block-two {
            --scene-h: 150;
            --scene-w: 150;
            position: relative;
            left: 99.5%;
            top: -1845%;
            clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            transform: rotate(-90deg);
            background: #3B2A6F;
            background: linear-gradient(to bottom, #3B2A6F 0% 6%, #0D0B40 6% 100%);
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 999
        }

        .leg-two {
            --scene-h: 4.25;
            --scene-w: 4.25;
            position: relative;
            left: 5%;
            top: 20%;
            background: red;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 9999
        }

        .scene {
            --scene-h: 19;
            --scene-w: 29;
            position: fixed;
            left: -38vw;
            top: -4vw;
            background-color: red;
            background: #3B2A6F;
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: 99999
        }

        .leg {
            --scene-h: 30;
            --scene-w: 1.4;
            position: relative;
            left: 20%;
            top: -443%;
            background: #3B2A6F;
            border-radius: 500px;
            background: linear-gradient(-20deg, #D3D6E5 0% 97%, #3B2A6F 97%);
            transform: rotate(20deg);
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin)
        }

        .leg-two {
            --scene-h: 30;
            --scene-w: 1.4;
            position: relative;
            left: 80%;
            top: -601%;
            background: #3B2A6F;
            border-radius: 500px;
            background: linear-gradient(20deg, #D3D6E5 0% 97%, #3B2A6F 97%);
            transform: rotate(-20deg);
            width: calc(var(--scene-w) * 1vmin);
            height: calc(var(--scene-h) * 1vmin);
            z-index: -1
        }

        .b {
            border-bottom-color: #4A2CDE
        }

        .c {
            background: transparent
        }

        .scene {
            cursor: pointer
        }

        .scene:not(:last-child):hover {
            cursor: pointer
        }

        .d {
            background: #4A2CDE
        }

        .unit {
            position: fixed;
            --h: 13;
            --w: 10;
            border-radius: .05rem;
            background-color: #DDD;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            left: -37vw;
            top: -3vw
        }

        .unit:hover {
            cursor: pointer
        }

        .detail {
            --h: 1.4;
            --w: 4;
            border-radius: .05rem;
            position: relative;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            left: 5.5%;
            top: 85%
        }

        .two {
            --h: 1.35;
            --w: 7.25;
            border-radius: .05rem;
            background-color: #3B2A6F;
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: 6%;
            left: 9.5%
        }

        .three {
            --h: 1.35;
            --w: 7.25;
            border-radius: .05rem;
            background-color: #3B2A6F;
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: 10%;
            left: 9.5%
        }

        .four {
            --h: 1.35;
            --w: 7.25;
            border-radius: .05rem;
            background-color: #3B2A6F;
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: 15%;
            left: 9.5%
        }

        .five {
            --h: 2;
            --w: 2;
            position: relative;
            background-color: #3B2A6F;
            border-radius: 50%;
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -21%;
            left: 44.9%;
            z-index: 999
        }

        .six {
            --h: 2;
            --w: 2;
            border-radius: 50%;
            background-color: #3B2A6F;
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -10.9%;
            left: 44.75%;
            z-index: 999
        }

        .seven {
            --h: 3;
            --w: 3;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -45%;
            left: 43%
        }

        .eight {
            --h: 3;
            --w: 3;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -40%;
            left: 43%
        }

        .nine {
            --h: 1.35;
            --w: 1.35;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -73%;
            left: 58%
        }

        .ten {
            --h: 1.35;
            --w: 1.35;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -1.5%;
            left: 73%
        }

        .eleven {
            --h: 1.35;
            --w: 1.35;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -8.5%;
            left: 83%
        }

        .twelve {
            --h: 1.35;
            --w: 1.35;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, .8);
            width: calc(var(--w) * 1vmin);
            height: calc(var(--h) * 1vmin);
            top: -15.5%;
            left: 92%
        }

</style>
