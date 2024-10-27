// src/utils/message.js
import { ElMessage } from 'element-plus';

export const showMessage = (message, type = 'info') => {
  ElMessage({
    message,
    type,
    duration: 1300, // 0.9秒后自动消失
    center: true // 居中显示
  });
};
