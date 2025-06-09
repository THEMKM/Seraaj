import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export interface SnackbarProps {
  message: string;
  open: boolean;
  onClose: () => void;
  actionLabel?: string;
  onAction?: () => void;
}

export default function Snackbar({ message, open, onClose, actionLabel, onAction }: SnackbarProps) {
  useEffect(() => {
    if (!open) return;
    const t = setTimeout(onClose, 3000);
    return () => clearTimeout(t);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed bottom-4 left-4 rounded-2xl bg-gray-800 text-white px-4 py-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
        >
          {message}
          {actionLabel && (
            <button className="ml-4 underline" onClick={onAction}>
              {actionLabel}
            </button>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
