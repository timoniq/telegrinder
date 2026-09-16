export const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

export const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, reducedMotion() ? 0 : ms));
