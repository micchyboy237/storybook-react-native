import { RenderContext } from '@storybook/types';

export interface PreviewError {
  message?: string;
  stack?: string;
}

export interface RequireContext {
  keys: () => string[];
  (id: string): any;
  resolve(id: string): string;
}
export type LoaderFunction = () => void | any[];
export type Loadable = RequireContext | RequireContext[] | LoaderFunction;

export type { RenderContext };

// The function used by a framework to render story to the DOM
export type RenderStoryFunction = (context: RenderContext) => void;
