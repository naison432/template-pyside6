from PySide6.QtWidgets import QComboBox


class Select(QComboBox):
    """
    Componente personalizado de QComboBox que incluye sus propios estilos.
    """

    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """
        /* =============================================== */
        /* COMBOBOX (Select) - PREMIUM STYLE               */
        /* =============================================== */
        QComboBox {
            background-color: #27272a; /* Zinc 800 - Contrast against 700/900 */
            border: 1px solid #52525b; /* Zinc 600 - Visible border */
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            color: #f4f4f5; /* Zinc 100 - High legibility */
        }

        QComboBox:hover {
            border: 1px solid #a1a1aa; /* Zinc 400 - Highlight on hover */
            background-color: #27272a; 
        }

        QComboBox:on { /* state when popup is open */
            border: 1px solid #d4d4d8; /* Zinc 300 - Active state */
            background-color: #27272a;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 0px;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
        }

        /* Flecha usando icono SVG */
        QComboBox::down-arrow {
            image: url(assets/icons/chevron_down.svg);
            width: 24px;
            height: 24px;
            margin-right: 10px;
        }

        QComboBox::down-arrow:on {
            image: url(assets/icons/chevron_up.svg);
            width: 24px;
            height: 24px;
            margin-right: 10px;
        }

        /* La lista desplegable */
        QComboBox QAbstractItemView {
            background-color: #18181b; /* Zinc 900 - Darker than input */
            border: 1px solid #52525b; /* Zinc 600 */
            selection-background-color: #3f3f46; /* Zinc 700 - Distinct selection */
            selection-color: #ffffff;
            outline: none;
            color: #d4d4d8; /* Zinc 300 - Readable items */
            border-radius: 6px;
            padding: 4px;
            margin-top: 4px; 
        }

        QComboBox QAbstractItemView::item {
            padding: 8px 10px;
            border-radius: 4px;
            margin: 2px;
        }

        QComboBox QAbstractItemView::item:hover {
            background-color: #27272a; /* Zinc 800 */
            color: #ffffff;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #3f3f46; /* Zinc 700 - Highlight */
            color: #ffffff;
            font-weight: 600;
        }
            """
        )
