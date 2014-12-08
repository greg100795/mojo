// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef EXAMPLES_WM_FLOW_WM_FRAME_CONTROLLER_H_
#define EXAMPLES_WM_FLOW_WM_FRAME_CONTROLLER_H_

#include "base/memory/scoped_ptr.h"
#include "mojo/services/public/cpp/view_manager/view_observer.h"
#include "services/window_manager/focus_controller.h"
#include "ui/gfx/geometry/rect.h"

namespace mojo {
class NativeWidgetViewManager;
class Shell;
class View;
}

namespace views {
class View;
class Widget;
}

namespace window_manager {
class WindowManagerApp;
}

// FrameController encapsulates the window manager's frame additions to a window
// created by an application. It renders the content of the frame and responds
// to any events targeted at it.
class FrameController : mojo::ViewObserver {
 public:
  FrameController(mojo::Shell* shell,
                  mojo::View* view,
                  mojo::View** app_view,
                  window_manager::WindowManagerApp* window_manager_app);
  virtual ~FrameController();

  void CloseWindow();
  void ToggleMaximize();

  void ActivateWindow();

 private:
  class LayoutManager;
  friend class LayoutManager;
  class FrameEventHandler;

  virtual void OnViewDestroyed(mojo::View* view) override;

  mojo::View* view_;
  mojo::View* app_view_;
  views::View* frame_view_;
  LayoutManager* frame_view_layout_manager_;
  views::Widget* widget_;
  bool maximized_;
  gfx::Rect restored_bounds_;
  window_manager::WindowManagerApp* window_manager_app_;
  scoped_ptr<FrameEventHandler> frame_event_handler_;

  DISALLOW_COPY_AND_ASSIGN(FrameController);
};

#endif  // EXAMPLES_WM_FLOW_WM_FRAME_CONTROLLER_H_
