# PyQt5 기반 다기능 메모장 개발 과정 (Gemini CLI와 함께)

이 문서는 Gemini CLI와 함께 PyQt5를 사용하여 다기능 메모장 애플리케이션을 개발한 과정을 요약합니다. 각 단계별로 추가된 기능, 구현 방식, 그리고 발생했던 주요 오류와 해결 방법을 기록합니다.

---

## 1. 기본 메모장 기능 구현

**요청:** 텍스트 입력/편집, 파일 열기/저장, 메뉴 바(새 파일, 열기, 저장, 다른 이름으로 저장, 끝내기), 상태 바(줄/열 번호)를 갖춘 기본적인 메모장 프로그램.

**구현:** `QMainWindow`, `QPlainTextEdit`, `QMessageBox`, `QFileDialog` 등을 사용하여 기본 UI와 파일 입출력 로직을 구현했습니다.

**주요 오류 및 해결:**

*   **오류 1:** `TypeError: cannot unpack non-iterable NoneType object`
    *   **원인:** 메뉴 항목을 정의한 딕셔너리/리스트에 구분선(`None`)을 포함했는데, `for` 루프에서 `None`을 튜플로 언팩(unpack)하려 시도하여 발생.
    *   **해결:** `for` 루프 내에서 각 항목이 `None`인지 먼저 확인하고, `None`이 아닐 경우에만 언팩하도록 로직을 수정했습니다.
*   **오류 2:** `TypeError: setShortcut(...) argument 1 has unexpected type 'NoneType'`
    *   **원인:** 단축키가 없는 메뉴 항목(`다른 이름으로 저장`)에 `None`을 단축키로 설정하려 시도하여 발생.
    *   **해결:** `QAction.setShortcut()` 호출 전에 단축키 값이 `None`이 아닌지 확인하는 조건을 추가했습니다.
*   **오류 3:** `RuntimeError: super-class __init__() of type Notepad was never called`
    *   **원인:** `Notepad` 클래스의 `__init__` 메서드에서 부모 클래스 생성자를 `super().__init__(self)`와 같이 잘못 호출하여 발생. 파이썬 3에서는 `super().__init__()`가 올바른 구문입니다.
    *   **해결:** `super().__init__(self)`를 `super().__init__()`로 수정했습니다.

---

## 2. 그림판 모드 및 확장 메뉴 추가

**요청:**
*   그림판 기능(펜, 색상, 굵기, 캔버스 지우기) 추가.
*   '그리기' 메뉴, '모드' 메뉴(텍스트/그림판 전환), '편집' 메뉴(실행 취소, 다시 실행, 잘라내기, 복사, 붙여넣기, 모두 선택), '서식' 메뉴(글꼴), '보기' 메뉴(상태 바 표시/숨기기, 자동 줄 바꿈) 추가.
*   상태 바에 모드별 정보 표시.

**구현:** `DrawingCanvas` 위젯을 새로 구현하고 `QStackedWidget`을 사용하여 텍스트 편집기와 그림판을 전환하도록 했습니다. 다양한 메뉴와 액션을 추가하고, 상태 바 업데이트 로직을 확장했습니다.

**주요 오류 및 해결:**

*   **오류 1:** `AttributeError: type object 'QIcon' has no attribute 'SP_FileIcon'`
    *   **원인:** `QIcon.SP_FileIcon`과 같이 `QIcon` 클래스에서 직접 표준 아이콘을 참조하려 시도하여 발생. 표준 아이콘은 `QStyle` 클래스를 통해 접근해야 합니다.
    *   **해결:** `PyQt5.QtWidgets`에서 `QStyle`을 임포트하고, `self.style().standardIcon(QStyle.SP_FileIcon)`과 같이 올바른 방식으로 아이콘을 참조하도록 수정했습니다.
*   **오류 2:** `AttributeError: type object 'QStyle' has no attribute 'SP_DialogCutButton'`
    *   **원인:** '잘라내기', '복사', '붙여넣기'에 해당하는 특정 표준 아이콘 이름이 `QStyle`에 존재하지 않아 발생.
    *   **해결:** 해당 액션들에서는 아이콘 지정을 제거하고 텍스트만 표시하도록 변경했습니다.
*   **오류 3:** `TypeError: unable to convert a QVariant of type 12 to a QMetaType of type 1025`
    *   **원인:** `QSettings`에서 창의 지오메트리(크기/위치)를 불러올 때 `type=bytes` 인자를 잘못 사용하여 발생.
    *   **해결:** `self.settings.value("geometry", ..., type=bytes)`에서 `type=bytes` 인자를 제거했습니다.
*   **오류 4 (반복):** 그림판 모드 전환 시 프로그램 종료.
    *   **원인:** `DrawingCanvas` 위젯의 초기화 시점과 크기 설정 문제, 그리고 모드 전환 로직의 복잡성 및 불안정한 이벤트 처리 방식(lambda 사용)이 복합적으로 작용하여 충돌 발생.
    *   **해결:**
        *   `DrawingCanvas` 초기화 시 기본 크기를 명시적으로 지정하여 안정성을 확보했습니다.
        *   `pyqtSignal`을 사용하여 위젯 간의 통신을 표준적이고 안전한 방식으로 변경했습니다.
        *   모드 전환 로직(`handle_mode_change`)을 단순화하고, `maybe_save` 처리 후 메뉴 상태 복구 로직을 명확히 했습니다.
        *   `QAction` 생성 시 `data` 키워드 인자 대신 `setData()` 메서드를 사용하도록 수정했습니다.
        *   `QActionGroup`에 액션을 추가할 때 `addActions()` 대신 `addAction()`을 사용하도록 수정했습니다.
        *   모드 메뉴의 `QAction`들이 메뉴에 실제로 추가되지 않아 클릭할 수 없었던 문제를 해결했습니다.
*   **오류 5:** `AttributeError: 'GlobalColor' object has no attribute 'name'`
    *   **원인:** `Qt.black`과 같은 `GlobalColor` 열거형 값에는 `name()` 메서드가 없는데, 이를 호출하려 시도하여 발생. `name()`은 `QColor` 객체에만 존재합니다.
    *   **해결:** `DrawingCanvas`에서 펜 색상을 `QColor(Qt.black)`으로 초기화하고, `PyQt5.QtGui`에서 `QColor`를 임포트했습니다.

---

## 3. 텍스트 편집기 기능 강화 (줄 번호, 단어 수, 줄 이동)

**요청:**
*   텍스트 편집기 왼쪽에 줄 번호 표시.
*   상태 바에 단어 수 표시.
*   특정 줄로 이동하는 기능.

**구현:**
*   `LineNumberArea` 위젯을 구현하여 줄 번호를 표시하고 `QPlainTextEdit`과 동기화했습니다.
*   `update_status_bar` 함수를 수정하여 단어 수를 계산하고 표시했습니다.
*   `go_to_line` 메서드와 메뉴 액션을 추가하여 줄 이동 기능을 구현했습니다.

**주요 오류 및 해결:**

*   **오류 1:** `AttributeError: type object 'Qt' has no attribute 'QSize'`
    *   **원인:** `QSize` 클래스를 `Qt` 모듈의 속성으로 잘못 참조하여 발생. `QSize`는 `PyQt5.QtCore`에서 직접 임포트해야 합니다.
    *   **해결:** `PyQt5.QtCore`에서 `QSize`를 임포트하고, `LineNumberArea`에서 `QSize(...)`를 직접 사용하도록 수정했습니다.
*   **오류 2 (반복):** `AttributeError: 'QPlainTextEdit' object has no attribute 'lineNumberAreaWidth'`
    *   **원인:** `LineNumberArea` 클래스 내에서 `self.editor.lineNumberAreaWidth()`를 호출했는데, `lineNumberAreaWidth`는 `QPlainTextEdit`의 메서드가 아니라 `LineNumberArea` 자체의 메서드입니다.
    *   **해결:** `LineNumberArea` 클래스에 `lineNumberAreaWidth()` 메서드를 추가하고, `sizeHint`에서 `self.lineNumberAreaWidth()`로 올바르게 호출하도록 수정했습니다.

---

## 4. 마크다운 미리보기 기능 추가

**요청:** 텍스트 모드에서 마크다운 문법으로 작성된 내용을 실시간으로 HTML 미리보기로 보여주는 기능.

**구현:**
*   `QTextBrowser` 위젯을 사용하여 미리보기 패널을 구현했습니다.
*   `보기` 메뉴에 '마크다운 미리보기' 체크박스 액션을 추가하여 패널을 토글할 수 있도록 했습니다.
*   `editor.textChanged` 시그널에 연결하여 `markdown` 라이브러리를 통해 텍스트를 HTML로 변환하고 미리보기를 업데이트했습니다.

**주요 오류 및 해결:**

*   **오류 1:** `markdown` 라이브러리 미설치.
    *   **원인:** `markdown` 라이브러리가 파이썬 환경에 설치되어 있지 않아 `ModuleNotFoundError` 발생.
    *   **해결:** `requirements.txt`에 `markdown`을 추가하고, 사용자에게 `pip install markdown` 명령어를 통해 설치하도록 안내했습니다.

---

## 5. 그림판 레이어 기능 추가

**요청:** 그림판 모드에서 여러 개의 레이어를 생성, 삭제, 순서 변경, 숨기기/보이기, 선택할 수 있는 기능.

**구현:**
*   `DrawingCanvas` 클래스를 수정하여 `self.layers` 리스트로 여러 `QPixmap` 객체를 관리하도록 했습니다.
*   '레이어' 메뉴를 새로 추가하고, 레이어 관리 액션들을 구현했습니다.
*   파일 열기/저장 로직을 업데이트하여 레이어를 처리하도록 했습니다.

**주요 오류 및 해결:**

*   **오류 1:** `AttributeError: 'DrawingCanvas' object has no attribute 'canvas'`
    *   **원인:** 레이어 기능 추가 과정에서 `DrawingCanvas` 내의 `self.canvas` (단일 픽스맵)와 `self.layers` (레이어 리스트) 간의 역할이 모호해져, 존재하지 않는 `self.canvas`를 참조하려 시도하여 발생.
    *   **해결:** `DrawingCanvas`에서 `self.canvas` 속성을 완전히 제거하고, 모든 그림 데이터는 `self.layers` 리스트를 통해 관리하도록 코드를 재구성했습니다.
*   **오류 2:** `AttributeError: 'DrawingCanvas' object has no attribute 'drawing'`
    *   **원인:** 이전 수정 과정에서 `DrawingCanvas`의 `__init__` 메서드에서 `self.drawing`, `self.start_point`, `self.end_point`와 같은 필수 속성들의 초기화가 누락되어 발생.
    *   **해결:** `DrawingCanvas.__init__`에 해당 속성들을 다시 명시적으로 초기화하는 코드를 추가했습니다.

---

## 현재 상태

현재 메모장 애플리케이션은 다음과 같은 기능을 제공합니다:

*   **텍스트 모드:**
    *   기본 텍스트 편집 (새 파일, 열기, 저장, 다른 이름으로 저장)
    *   실행 취소/다시 실행, 잘라내기/복사/붙여넣기, 찾기/바꾸기
    *   글꼴 변경
    *   줄 번호 표시
    *   단어 수 표시
    *   줄 이동
    *   마크다운 실시간 미리보기
*   **그림판 모드:**
    *   펜, 지우개, 직선, 사각형, 원 그리기 도구
    *   펜 색상 및 굵기 변경
    *   도형 채우기
    *   캔버스 지우기
    *   **레이어 관리 (추가, 삭제, 순서 변경, 숨기기/보이기, 선택)**
*   **공통 기능:**
    *   모드 전환 (텍스트/그림판)
    *   툴바
    *   상태 바 (모드별 정보, 커서 위치, 단어 수, 펜/도구/레이어 정보)
    *   최근에 연 파일 목록
    *   창 크기/위치 설정 저장 및 복원
    *   종료 시 변경 내용 저장 확인

---

## 향후 추가 가능한 기능

*   **그림판 모드 - 그리기 실행 취소/다시 실행 (Undo/Redo for Drawing):** 현재는 텍스트 모드에만 적용되어 있습니다.
*   **일반 - "다크 모드" 토글:** 사용자 편의성을 위한 테마 변경 기능.
*   **일반 - 정보 (About) 대화 상자:** 프로그램 정보 표시.
*   **텍스트 모드 - 구문 강조 (Syntax Highlighting):** 코드 편집 시 유용.
*   **텍스트 모드 - 통합 코드 스니펫 관리자:** 자주 사용하는 코드 조각 저장 및 삽입.

---
