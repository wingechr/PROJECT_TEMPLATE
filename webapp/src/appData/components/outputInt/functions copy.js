function setValue(e, v) {
  e.textContent = v.toLocaleString("de-DE", {
    useGrouping: true,
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
}

export default { setValue };
