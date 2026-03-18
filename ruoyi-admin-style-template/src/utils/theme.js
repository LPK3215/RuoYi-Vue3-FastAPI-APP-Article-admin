export function handleThemeStyle(theme) {
  const [red, green, blue] = hexToRgb(theme)
  document.documentElement.style.setProperty('--el-color-primary', theme)
  document.documentElement.style.setProperty('--app-primary-color', theme)
  document.documentElement.style.setProperty('--app-primary-rgb', `${red} ${green} ${blue}`)
  for (let index = 1; index <= 9; index += 1) {
    document.documentElement.style.setProperty(`--el-color-primary-light-${index}`, getLightColor(theme, index / 10))
    document.documentElement.style.setProperty(`--el-color-primary-dark-${index}`, getDarkColor(theme, index / 10))
  }
}

export function hexToRgb(color) {
  const hex = color.replace('#', '')
  const values = hex.match(/../g) || ['0', '0', '0']
  return values.map((item) => Number.parseInt(item, 16))
}

export function rgbToHex(red, green, blue) {
  return `#${[red, green, blue]
    .map((value) => value.toString(16).padStart(2, '0'))
    .join('')}`
}

export function getLightColor(color, level) {
  const rgb = hexToRgb(color)
  return rgbToHex(
    Math.floor((255 - rgb[0]) * level + rgb[0]),
    Math.floor((255 - rgb[1]) * level + rgb[1]),
    Math.floor((255 - rgb[2]) * level + rgb[2]),
  )
}

export function getDarkColor(color, level) {
  const rgb = hexToRgb(color)
  return rgbToHex(
    Math.floor(rgb[0] * (1 - level)),
    Math.floor(rgb[1] * (1 - level)),
    Math.floor(rgb[2] * (1 - level)),
  )
}
